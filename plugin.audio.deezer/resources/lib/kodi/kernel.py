from . import xbmcplugin

try:
    import importlib
except ImportError:
    import kodi.importlib as importlib

from utils import Utils
from di import ServiceContainer
from router import Router, RuleNotFoundError
from request import Request
from response import NotFoundResponse, ErrorResponse

class Kernel(object):
    """
    @type _config: dict
    @type _utils: Utils
    @type _service_container: ServiceContainer
    @type _router: Router
    """

    def __init__(self, config):
        self._config = config
        self._utils = Utils(self)
        self._service_container = ServiceContainer(self)
        self._router = Router(self)

    def get_config(self, name):
        """@rtype: dict|str"""
        return self._config[name]

    def get_utils(self):
        """@rtype: Utils"""
        return self._utils

    def get_service_container(self):
        """@rtype: ServiceContainer"""
        return self._service_container

    def get_router(self):
        """@rtype: Router"""
        return self._router

    def handle(self, request):
        """@type request: Request"""
        try:
            rule, keys = self._router.match(request.get_path())
            target = rule['target'].split(':')

            MyController = getattr(importlib.import_module(rule['module']), target[0])
            controller = MyController(self, request)
            method = getattr(controller, target[1])
            return method(**keys)
        except RuleNotFoundError:
            return NotFoundResponse(self, request.get_path())
        except Exception as e:
            return ErrorResponse(self, e)

    def terminate(self, request, response, success):
        xbmcplugin.endOfDirectory(request.get_id(), succeeded=success)


# from resources.lib.routing.router import route, router
#
# @route('/user/<user>/tracks/<track>', name='get_tracks')
# def get_tracks(user, track=None):
#     print "show_track %s %s" % (user, track)
#
#
# print router.match('/user/kubatek94/tracks/')