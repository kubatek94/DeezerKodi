from .View import View

import os
import xbmc
import xbmcgui
import xbmcplugin


class ArtistTopView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(ArtistTopView, self).__init__(scene, view_router, "artisttop", parent_view)
        self.lazyTop = None

    def _get_lazy_top(self):
        # try to get lazy top from the parent if none are set
        if self.lazyTop is None:
            self.lazyTop = self.parent_view.get_lazy_top()
        return self.lazyTop

    def _show_top(self):
        self.top_tracks = self._get_lazy_top()()
        list_items = []

        for i in range(0, len(self.top_tracks)):
            try:
                track = self.top_tracks[i]
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title),
                                             thumbnailImage=track.album.cover_big)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url("/tracks/%d" % track.id), list_item, False))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)
        xbmcplugin.setContent(self.scene.scene_router.addon_handle, 'songs')

    def show(self):
        self._show_top()


class ArtistMenuView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(ArtistMenuView, self).__init__(scene, view_router, "artistmenu", parent_view)

    def get_lazy_albums(self):
        artist = self.parent_view.get_artist()
        return lambda: self.scene.cache.get('artistalbums_%s' % artist.id, default_producer=artist.get_albums)

    def get_lazy_playlists(self):
        artist = self.parent_view.get_artist()
        return lambda: self.scene.cache.get('artistplaylists_%s' % artist.id, default_producer=artist.get_playlists)

    def get_lazy_radio(self):
        artist = self.parent_view.get_artist()
        return lambda: self.scene.cache.get('artistradio_%s' % artist.id, default_producer=artist.get_radio)

    def get_lazy_top(self):
        artist = self.parent_view.get_artist()
        return lambda: self.scene.cache.get('artisttop_%s' % artist.id, default_producer=artist.get_top)

    # to display the radio as tracks
    def get_list_items(self):
        artist = self.parent_view.get_artist()
        list_items = []
        for track in self.scene.cache.get('artistradio_%s' % artist.id, default_producer=artist.get_radio):
            try:
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title),
                                             thumbnailImage=track.album.cover_big)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': track.artist.picture_big})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url("/%d" % track.id), list_item, False))
            except:
                pass
        return list_items

    def _show_menu(self):
        items = {
            3000: {
                "image": xbmc.translatePath(
                    os.path.join(self.scene.scene_router.images_path, "genre-button.png")),
                "url": self.get_url("/artisttop")
            },
            3001: {
                "image": xbmc.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myalbums-button.png")),
                "url": self.get_url("/albums")
            },
            3002: {
                "image": xbmc.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "myplaylists-button.png")),
                "url": self.get_url("/playlists")
            },
            3003: {
                "image": xbmc.translatePath(os.path.join(self.scene.scene_router.images_path,
                                                         "radiochannels-button.png")),
                "url": self.get_url("/tracks")
            }
        }
        artist = self.parent_view.get_artist()
        list_items = []
        for item in items:
            try:
                list_item = xbmcgui.ListItem(self.scene.scene_router.language(item), iconImage=items[item]["image"])
                list_item.setArt({'fanart': artist.picture_big})
                list_items.append((items[item]["url"], list_item, True))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def show(self):
        self._show_menu()


class ArtistsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(ArtistsView, self).__init__(scene, view_router, "artists", parent_view)
        self.lazy_artists = None

    def set_lazy_artists(self, lazy_artists):
        self.lazy_artists = lazy_artists

    def _get_lazy_artists(self):
        # try to get lazy artists from the parent if none are set
        if self.lazy_artists is None:
            self.lazy_artists = self.parent_view.get_lazy_artists()
        return self.lazy_artists

    def get_artist(self):
        self.artists = self._get_lazy_artists()()
        return self.artists[self.id]

    def _showArtists(self):
        self.artists = self._get_lazy_artists()()
        list_items = []

        for i in range(0, len(self.artists)):
            try:
                artist = self.artists[i]
                list_item = xbmcgui.ListItem(artist.name, thumbnailImage=artist.picture_big)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                list_items.append((self.get_url("/%d/artistmenu" % i), list_item, True))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def show(self):
        self._showArtists()
