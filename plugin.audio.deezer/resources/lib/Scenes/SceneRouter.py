import urlparse
import xbmcplugin
import xbmc
import xbmcgui
import xbmcaddon
import os

from .MainScene import MainScene
from .RadioChannelsScene import RadioChannelsScene
from .MyPlaylistsScene import MyPlaylistsScene
from .MyAlbumsScene import MyAlbumsScene
from .MyArtistsScene import MyArtistsScene
from .SearchScene import SearchScene
from .ChartScene import ChartScene

from ..DeezerApi import Connection, Api
from ..cache import Cache


class SceneRouter(object):
    def __init__(self):
        self.addon = xbmcaddon.Addon('plugin.audio.deezer')
        self.language = self.addon.getLocalizedString
        self.addon_path = self.addon.getAddonInfo('path')
        self.resources_path = xbmc.translatePath(os.path.join(self.addon_path, 'resources'))
        self.images_path = xbmc.translatePath(os.path.join(self.resources_path, 'img'))
        self.fanart_path = xbmc.translatePath(os.path.join(self.addon_path, 'fanart.jpg'))
        self.cache = Cache("deezerapi")

        self.scenes = {
            "main": lambda: MainScene(self),
            "chart": lambda: ChartScene(self),
            "radiochannels": lambda: RadioChannelsScene(self),
            "playlists": lambda: MyPlaylistsScene(self),
            "albums": lambda: MyAlbumsScene(self),
            "artists": lambda: MyArtistsScene(self),
            "search": lambda: SearchScene(self)
        }

    # url consists of the path and query parts
    def get_url(self, scene=None):
        return {'path': self.get_path(scene), 'query': self.get_query(scene)}

    def set_url(self, url):
        full_url = "%s?%s" % (url['path'], url['query'])
        self.args['path'] = [full_url]

    # path consists of e.g. /search/3000/tracks/1
    def get_path(self, scene=None):
        path = None
        if scene is None:
            path = self.args.get('path', ["/"])[0]
        else:
            path = self.args.get('path', ["/%s" % scene.name])[0]
        return path.split('?')[0]

    def set_path(self, path):
        url = {'path': path, 'query': self.get_query()}
        self.set_url(url)

    def set_query(self, query):
        url = {'path': self.get_path(), 'query': query}
        self.set_url(url)

    # query consists of e.g. searchQuery=Hello&foo=bar
    def get_query(self, scene=None):
        path = None
        if scene is None:
            path = self.args.get('path', ["/"])[0]
        else:
            path = self.args.get('path', ["/%s" % scene.name])[0]
        s = path.split('?')
        if len(s) > 1:
            return s[1]
        else:
            return ''

    def notification(self, header, message):
        command = 'Notification(%s, %s)' % (header, message)
        xbmc.executebuiltin(command)

    def _has_credentials(self):
        self._username = self.addon.getSetting('username')
        self._password = self.addon.getSetting('password')
        if self._username != "" and self._password != "":
            return self.connect()
        else:
            return False

    def _check_credentials(self):
        if not self._has_credentials():
            dialog = xbmcgui.Dialog()

            while True:
                self.addon.openSettings()
                if not self._has_credentials():
                    # Sign in required | Do you want to try again, or exit Deezer? | Try again | Exit
                    try_again = dialog.yesno(self.language(2006), self.language(2008), yeslabel=self.language(2009),
                                             nolabel=self.language(2010))
                    if not try_again:
                        return False
                else:
                    return True
        return True

    def get_user(self):
        self.user = self.cache.get('user', default_producer=lambda: self.api.get_user())
        return self.user

    def connect(self):
        try:
            self.connection = self.cache.get('connection',
                                             default_producer=lambda: Connection(self._username, self._password))
        except Exception as e:
            self.notification("Could not sign in", e)
            return False
        return True

    def route(self, argv):
        self.base_url = argv[0]
        self.addon_handle = int(argv[1])
        self.args = urlparse.parse_qs(argv[2][1:])

        is_signed_in = self._check_credentials()

        if is_signed_in:
            self.api = self.cache.get('api', default_producer=lambda: Api(self.connection))

            scene_type = self.args.get('scene', ['main'])[0]
            scene = self.scenes.get(scene_type, None)

            if scene is not None:
                scene()

        xbmcplugin.endOfDirectory(self.addon_handle, succeeded=is_signed_in)
        self.cache.save()
