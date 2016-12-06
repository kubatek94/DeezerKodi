import sys
import importlib
from utils import Utils
from di import ServiceContainer
from router import Router, RuleNotFoundError
from request import Request
from response import Response

class Kernel(object):

    def __init__(self, config):
        self._config = config
        self._utils = Utils(self)
        self._service_container = ServiceContainer(self)
        self._router = Router(self)

    def get_config(self, name):
        return self._config[name]

    def handle(self, request):
        try:
            rule, keys = self._router.match(request.get_path())
            target = rule['target'].split(':')

            MyClass = getattr(importlib.import_module(rule['module']), target[0])
            controller = MyClass(self)
            method = getattr(controller, target[1])
            return method(**keys)
        except RuleNotFoundError:
            self._utils.notify('404', 'There is no handler for the url ==> %s' % request.get_path())
            return Response(self)

    def terminate(self, request, response):
        self._utils.notify('End', 'Terminate request')


# from resources.lib.routing.router import route, router
#
# @route('/user/<user>/tracks/<track>', name='get_tracks')
# def get_tracks(user, track=None):
#     print "show_track %s %s" % (user, track)
#
#
# print router.match('/user/kubatek94/tracks/')