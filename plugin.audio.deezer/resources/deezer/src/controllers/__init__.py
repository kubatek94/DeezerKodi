from kodi.controller import Controller
from kodi.response import Response


class IndexController(Controller):
    def index(self):
        xbmc = self.get('kodi.xbmc')

        dialog = self.get('kodi.xbmc.gui').Dialog()
        ret = dialog.contextmenu(['Yes', 'No'])

        xbmc.notify('Results', 'You selected: %s' % ret)
        return Response()
