ccm_api_url = 'http://localhost:7788/api/v0'

ccm_api_args = {
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
    'deviceobject.create': ['p_id', 'dm_name', 'dfs'],
    'deviceobject.get': ['p_id', 'do_id'],
    'deviceobject.delete': ['p_id', 'do_id'],
    'networkapplication.create': ['p_id', 'joins'],
    'networkapplication.get': ['p_id', 'na_id'],
    'networkapplication.delete': ['p_id', 'na_id'],
    'device.get': ['p_id', 'do_id'],
    'device.bind': ['p_id', 'do_id', 'd_id'],
    'device.unbind': ['p_id', 'do_id']
}
