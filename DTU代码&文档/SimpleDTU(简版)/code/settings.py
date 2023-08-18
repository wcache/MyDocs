try:
    import ujson as json
except Exception:
    import json


class Settings(object):

    def __init__(self, path='config.json'):
        self.config_path = path
        self.__settings = None
        self.load()  # first load setting from json file.

    def __str__(self):
        return str(self.__settings)

    def load(self, reload=False):
        if (self.__settings is None) or reload:
            self.__settings = self.__read_config()

    def __read_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get(self, key_string):
        return self.__recurse_handler(
            self.__settings,
            key_string.split('.'),
            operate='get'
        )

    def set(self, key_string, value):
        return self.__recurse_handler(
            self.__settings,
            key_string.split('.'),
            value=value,
            operate='set'
        )

    def delete(self, key_string):
        keys = key_string.split('.')
        return self.__recurse_handler(
            self.__settings,
            keys,
            operate='delete'
        )

    def __recurse_handler(self, settings, keys, value=None, operate=''):
        if len(keys) == 0:
            return

        if not isinstance(settings, dict):
            raise TypeError('config item \"{}\" is not valid(DictLike).'.format(settings))

        key = keys.pop(0)

        if len(keys) == 0:
            if operate == 'get':
                return settings[key]
            elif operate == 'set':
                settings[key] = value
            elif operate == 'delete':
                del settings[key]
            return

        if key not in settings:
            if operate == 'set':
                settings[key] = {}  # auto create sub items recursively.
            else:
                return

        return self.__recurse_handler(settings[key], keys, value=value, operate=operate)

    def save(self):
        with open(self.config_path, 'w+', encoding='utf-8') as f:
            return json.dump(self.__settings, f)


config = Settings('/usr/dtu_config.json')
