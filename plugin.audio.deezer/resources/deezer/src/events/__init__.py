from kodi.event import EventSubscriber
from kodi.events import KernelEvents
from kodi.response import Response


class LoginGatewaySubscriber(EventSubscriber):
    def get_events(self):
        return [(KernelEvents.REQUEST, self.verify_credentials)]

    def verify_credentials(self, event):
        dialog = self.get('kodi.xbmc.gui').Dialog()

        self.get('deezer.api')

        # while True:
        #     try:
        #         self.get('deezer.api')
        #         break
        #     except:
        #         retry = dialog.yesno('Error. Could not authenticate.', 'Would you like to check your credentials and re-try?')
        #         if retry:
        #             self.get('kodi.xbmc.addon').openSettings()
        #         else:
        #             response = Response(success=False)
        #             event.set_response(response)
        #             return

        self.get('kodi.xbmc').notify('Success', 'Logged in as %s' % self.get_parameter('deezer.api.username'))