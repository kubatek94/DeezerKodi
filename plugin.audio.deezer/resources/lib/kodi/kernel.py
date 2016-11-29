import sys
import utils
from request import Request

class Kernel(object):

    def __init__(self, env):
        self._name = 'plugin.audio.deezer'
        self._env = env


    def boot(self):
        if self._env == 'mock':
            sys.argv = ['', -1, '']
        self._request = Request.create_from_globals()


# from resources.lib.routing.router import route, router
#
# @route('/user/<user>/tracks/<track>', name='get_tracks')
# def get_tracks(user, track=None):
#     print "show_track %s %s" % (user, track)
#
#
# print router.match('/user/kubatek94/tracks/')