from kodi.response import Response

class AskCredentialsResponse(Response):
    def send(self):
        xbmc = self.get('kodi.xbmc')
        xbmc.notify('Error', 'Could not authenticate. Please check your details')

        addon = self.get('kodi.xbmc.addon')
        addon.openSettings()