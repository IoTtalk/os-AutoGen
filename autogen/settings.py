from .settings import *  # noqa: F401,F403 imported but unused,import shared settings, F401

SECRET_KEY = 'qsq%%HG*Cww!06!l?7=\\~SL!"b+2Ut_r{j?Y,)#CzafQb2H3Ojb'

ROOT_URLCONF = 'autogen.urls'

INSTALLED_APPS += []

MIDDLEWARE += [
    'autogen.middleware.JsonRequestMiddleware',
]

CCM_API_URL = 'http://localhost:7788/api/v0'

CCM_API_ARGS = {
    'account.create': ['username', 'password'],
    'account.login': ['uesrname', 'password'],
    'account.delete': [],
    'account.profile': [],
    'devicefeature.create': ['df_name', 'type', 'parameter'],
    'devicefeature.get': ['df'],
    'devicefeature.update': ['df_id', 'df_name', 'df_type', 'parameter'],
    'devicefeature.delete': ['df'],
    'devicemodel.create': ['dm_name', 'dfs'],
    'devicemodel.get': ['dm'],
    'devicemodel.update': ['dm_id', 'dm_name', 'dfs'],
    'devicemodel.delete': ['dm'],
    'project.create': ['p_name'],
    'project.get': ['p_id'],
    'project.delete': ['p_id'],
    'project.on': ['p_id'],
    'project.off': ['p_id'],
    'simulation.get': ['p_id'],
    'simulation.on': ['p_id'],
    'simulation.off': ['p_id'],
    'deviceobject.create': ['p_id', 'dm_name', 'dfs'],
    'deviceobject.get': ['p_id', 'do_id'],
    'deviceobject.delete': ['p_id', 'do_id'],
    'devicefeatureobject.get': ['p_id', 'do_id', 'dfo_id'],
    'devicefeatureobject.update': ['p_id', 'do_id', 'dfo_id', 'alias_name', 'df_parameter'],
    'function.create': ['fn_name', 'code'],
    'function.update': ['fn_id', 'code'],
    'function.delete': ['fn_id'],
    'function.list': [],
    'function.list_df': ['df_id'],
    'function.list_na': [],
    'function.get': ['fn_id'],
    'function.get_all_versions': ['fn_id'],
    'function.get_version': ['fnvt_idx'],
    'function.create_sdf': ['fn_id'],
    'function.delete_sdf': ['fn_id'],
    'networkapplication.create': ['p_id', 'joins'],
    'networkapplication.get': ['p_id', 'na_id'],
    'networkapplication.update': ['p_id', 'na_id', 'dfm_list'],
    'networkapplication.delete': ['p_id', 'na_id'],
    'device.get': ['p_id', 'do_id'],
    'device.bind': ['p_id', 'do_id', 'd_id'],
    'device.unbind': ['p_id', 'do_id'],
    'alias.get': ['mac_addr', 'df_name'],
    'alias.set': ['mac_addr', 'df_name', 'alias_name']
}

# configure ccm api in global
#
import ccmapi.v0 as ccmapi

ccmapi.config.config.api_url = CCM_API_URL
