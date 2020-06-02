import requests

import ccmapi.v0 as api

from .config import ccm_api_password, ccm_api_url, ccm_api_username
from .utils import rgetattr


api.config.api_url = ccm_api_url


class _CcmApiHandler():
    api_args = {
        'account.create': ['username', 'password'],
        'account.login': ['uesrname', 'password'],
        'account.delete': [],
        'account.profile': [],
        'devicefeature.create': ['df_name', 'type', 'parameter'],
        'devicefeature.get': ['df_id'],
        'devicefeature.delete': ['df_id'],
        'devicemodel.create': ['dm_name', 'dfs'],
        'devicemodel.get': ['dm_id'],
        'devicemodel.delete': ['dm_id'],
        'project.create': ['p_name'],
        'project.get': ['p_id'],
        'project.delete': ['p_id'],
        'project.on': ['p_id'],
        'project.off': ['p_id'],
        'deviceobject.create': ['p_id', 'dm_name', 'df'],
        'deviceobject.get': ['p_id', 'do_id'],
        'networkapplication.create': ['p_id', 'joins'],
        'networkapplication.get': ['p_id', 'id'],
        'device.get': ['p_id', 'do_id'],
        'device.bind': ['p_id', 'do_id', 'd_id'],
        'device.unbind': ['p_id', 'do_id']
    }

    def __init__(self):
        self.s = requests.Session()
        self.u_id, self.cookie = api.account.login(
                                    ccm_api_username,
                                    ccm_api_password,
                                    session=self.s)

    def request(self, api_name, payload):
        # get api function from library ccmapi
        f = rgetattr(api, api_name)

        # extract args from payload
        args = [payload.pop(k) for k in self.api_args.get(api_name, [])]

        # assign logined session to invoke api
        payload.update({'session': self.s})

        return f(*args, **payload)

ccmapihandler = _CcmApiHandler()
