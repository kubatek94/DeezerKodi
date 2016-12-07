from ..kodi.response import Response
from ..kodi.controller import Controller

class Settings(Controller):

    def show_settings(self, user='me'):
        """
        @type: settings.Settings
        """
        settings = self.get('settings')
        settings.open()