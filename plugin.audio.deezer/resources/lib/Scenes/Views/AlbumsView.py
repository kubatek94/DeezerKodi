from .View import View

import xbmcgui
import xbmcplugin


class AlbumsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(AlbumsView, self).__init__(scene, view_router, "albums", parent_view)
        self.lazy_albums = None

    def set_lazy_albums(self, lazy_albums):
        self.lazy_albums = lazy_albums

    def _get_lazy_albums(self):
        # try to get lazy albums from the parent if none are set
        if self.lazy_albums is None:
            self.lazy_albums = self.parent_view.get_lazy_albums()
        return self.lazy_albums

    def _show_albums(self):
        self.albums = self._get_lazy_albums()()
        list_items = []

        for i in range(0, len(self.albums)):
            try:
                album = self.albums[i]
                list_item = xbmcgui.ListItem(album.title, thumbnailImage=album.cover_big)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                list_items.append((self.get_url("/%d/tracks" % i), list_item, True))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def get_list_items(self):
        self.albums = self._get_lazy_albums()()
        album = self.albums[self.id]
        list_items = []

        for track in album.get_tracks():
            try:
                list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title),
                                             thumbnailImage=album.cover_big)
                list_item.setProperty('IsPlayable', 'true')
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                self.add_item_track_info(list_item, track)
                list_items.append((self.get_url("/%d" % track.id), list_item, False))
            except:
                pass
        return list_items

    def show(self):
        self._show_albums()
