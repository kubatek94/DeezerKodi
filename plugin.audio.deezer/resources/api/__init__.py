import os
from kodi.config import YamlConfigLoader


def get_config(app):
    loader = YamlConfigLoader(app)
    return loader.load_config(os.path.join(__path__[0], 'config.yml'))


def register(app):
    pass
