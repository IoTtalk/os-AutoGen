IoTtalk AutoGen Subsystem
===============================================================================


Installation
----------------------------------------------------------------------

Install required package
::

    pip install -r requirements.txt

Migrate database
::

    ./manage.py migratesites

Modify Setting file, set the ccm host to your iottalk-ccm server.
::

    # in autogen/settings.py
    CCM_API_URL = 'http://<CCM_HOST>[:<CCM_PORT>]/api/v0'


Create Example XTalk
----------------------------------------------------------------------

#. Create a Django application ``footalk``::

    ./manage.py startapp footalk

#. Create ``footalk/settings.py`` for it as following::

    import os

    from .settings import *

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = 'my_very_secret_code'

    INSTALLED_APPS += [
        'footalk.apps.FootalkConfig',
    ]

    ROOT_URLCONF = 'footalk.urls'

    AG_API_URL = 'http://localhost:8080'

#. Install the settings file in the dir ``_``::

    cd _ && ln -s ../footalk/settings.py footalk_settings.py

#. Create ``footalk/urls.py`` for it as following::

    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]

#. Modify your ``footalk/views.py`` and create a view function ``index``::

    def index(request):
        ...

#. Migrate DB::

    ./manage.py makemigrations --settings=_.footalk_settings
    ./manage.py migrate --settings=_.footalk_settings

#. Start your FooTalk at port 8081 and the AutoGen Subsystem at port 8080::

    ./manage.py runsites -s autogen:8080 -s footalk:8081
