from .View import View
from .TracksView import TracksView

import xbmcgui
import xbmcplugin


class PlaylistsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(PlaylistsView, self).__init__(scene, view_router, "playlists", parent_view)
        self.lazy_playlists = None

    def set_lazy_playlists(self, lazy_playlists):
        self.lazy_playlists = lazy_playlists

    def _get_lazy_playlists(self):
        # try to get lazy playlists from the parent if none are set
        if self.lazy_playlists is None:
            self.lazy_playlists = self.parent_view.get_lazy_playlists()
        return self.lazy_playlists

    def _show_playlists(self):
        self.playlists = self._get_lazy_playlists()()
        list_items = []

        for i in range(0, len(self.playlists)):
            try:
                playlist = self.playlists[i]
                list_item = xbmcgui.ListItem(playlist.title, thumbnailImage=playlist.picture_big)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                list_items.append((self.get_url("/%d/tracks" % i), list_item, True))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def get_list_items(self):
        self.playlists = self._get_lazy_playlists()()
        playlist = self.playlists[self.id]
        list_items = []

        for track in playlist.get_tracks():
            try:
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title),
                                             thumbnailImage=track.album.cover_big)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': playlist.picture_big})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url("/%d" % track.id), list_item, False))
            except:
                pass
        return list_items

    def show(self):
        self._show_playlists()
