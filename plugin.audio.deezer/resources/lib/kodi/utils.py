from . import xbmc

class Utils(object):
    def __init__(self, kernel):
        self._kernel = kernel

    def notify(self, heading, message):
        command = 'Notification(%s, %s)' % (heading, message)
        xbmc.executebuiltin(command)