from . import xbmc

class Utils(object):

    def notify(self, heading, message):
        command = 'Notification(%s, %s)' % (heading, message)
        xbmc.executebuiltin(command)