from yaml import safe_load


class Config(object):
    def __init__(self, config_path, default_path=None):
        cfg = self._load_config(config_path)
        if default_path is not None:
            default_cfg = self._load_config(default_path)
        
        merge_dictionaries_recursively(default_cfg, cfg)
        self._data = cfg


    def _load_config(self, config_path):
        with open(config_path) as cf_file:
            return safe_load( cf_file.read() )
        

    def get(self, path=None, default=None, cast=None):
        sub_dict = dict(self._data)

        if (path is None):
            return sub_dict
        
        path_items = path.split("/")[:-1]
        data_item = path.split("/")[-1]
        
        try:
            for path_item in path_items:
                sub_dict = sub_dict.get(path_item)
            
            value = sub_dict.get(data_item, default)

            return cast(value) if cast else value
        except (TypeError, AttributeError, ValueError):
            return default



def merge_dictionaries_recursively(dict1, dict2):
    ''' Update two config dictionaries recursively.
    Args:
        dict1 (dict): first dictionary to be updated
        dict2 (dict): second dictionary which entries should be preferred
    '''

    if dict2 is None: return
    for k, v in dict2.items():
        if k not in dict1:
            dict1[k] = dict()
        if isinstance(v, dict):
            merge_dictionaries_recursively(dict1[k], v)
        else:
           dict1[k] = v