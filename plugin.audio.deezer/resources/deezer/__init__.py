import os
from kodi.config import YamlConfigLoader
from deezer.src.events import LoginGatewaySubscriber


def get_config(app):
    loader = YamlConfigLoader(app)
    return loader.load_config(os.path.join(__path__[0], 'config/config.yml'))


def register(app):
    event_dispatcher = app.container.get_service('kodi.event_dispatcher')
    login_gateway_subscriber = LoginGatewaySubscriber()
    login_gateway_subscriber.set_container(app.container)
    event_dispatcher.add_subscriber(login_gateway_subscriber)