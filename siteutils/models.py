import os
import shutil

import pygit2

from django.conf import settings
from django.db import models
from django.db.models import Q

from .exceptions import FileNotFound


class GitRepoManager(models.Manager):
    def create(self, *args, url=None, **kwargs):
        '''
        if a keyword argument ``url`` is given, we will clone repo from the remote.
        '''
        obj = super().create(*args, **kwargs)
        # https://www.pygit2.org/recipes/git-init.html#create-bare-repository
        if url is None:
            pygit2.init_repository(obj.repo_path, bare=True)
        else:
            pygit2.clone_repository(url, obj.repo_path, bare=True)
        return obj

    def available(self, user):
        return self.filter(Q(user=user) | Q(user_id=settings.SYSADMIN_UID))


class GitRepo(models.Model):
    class Meta:
        # https://docs.djangoproject.com/en/3.1/topics/db/models/#abstract-base-classes
        abstract = True
        unique_together = [('user', 'name')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    default_branch = models.CharField(max_length=1024, default='refs/heads/master')

    objects = GitRepoManager()

    @property
    def repo(self):
        return pygit2.Repository(self.repo_path)

    @property
    def repo_path(self):
        return os.path.join(self.repos_root, str(self.user.id), self.name)

    def delete(self, *args, **kwargs):
        path = self.repo_path
        ret = super().delete(args, **kwargs)
        shutil.rmtree(path)
        return ret

    def __str__(self):
        return f'{self.user.username}/{self.name}'

    @property
    def repos_root(self):
        return settings.REPOS_ROOT


class CodeRepoManager(GitRepoManager):
    def create(self, *args, **kwargs):
        obj = super().create(*args, **kwargs)
        repo = obj.repo
        if repo.head_is_unborn:
            # create root commit
            # https://gist.github.com/iblis17/ab906b52aea96ba6afc2517d5a9561e6
            # https://www.pygit2.org/objects.html?highlight=create_commit#creating-commits
            tree = repo.TreeBuilder()
            tree.insert(obj.entry, repo.create_blob(''), pygit2.GIT_FILEMODE_BLOB)
            sig = obj.git_sig
            repo.create_commit(
                obj.default_branch, sig, sig, 'Initial mommit', tree.write(), [])
        return obj


class CodeRepo(GitRepo):
    class Meta:
        abstract = True

    # the jupyter kernel name
    runtime = models.CharField(max_length=1024, default='python3')
    entry = models.CharField(max_length=1024, default='main.py')

    objects = CodeRepoManager()

    @property
    def git_sig(self):
        user = self.user
        return pygit2.Signature(user.username, user.email if user.email else user.username)

    @property
    def ext(self):
        _, ext = os.path.splitext(self.entry)
        return ext[1:]

    @property
    def is_ipynb(self):
        return 'ipynb' in self.ext

    @property
    def lang(self):
        '''
        Determine the language of program by file name extension
        '''
        _, ext = os.path.splitext(self.entry)
        map_ = {
            '.py': 'python',
            '.java': 'java',
        }
        return map_.get(ext)

    def commit(self, content: str, message: str = 'update by django'):
        repo = self.repo
        tree = repo.TreeBuilder()
        tree.insert(self.entry, repo.create_blob(content), pygit2.GIT_FILEMODE_BLOB)
        sig = self.git_sig
        return repo.create_commit(
            self.default_branch, sig, sig, message, tree.write(), [repo.head.target])

    def read(self, path):
        '''
        Read the file content
        '''
        repo = self.repo
        commit = repo[repo.head.target]
        tree = commit.tree
        if path not in tree:
            raise FileNotFound()
        return tree[path].data.decode()

    @property
    def content(self):
        return self.read(self.entry)
