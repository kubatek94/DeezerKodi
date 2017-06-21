from .View import View

import xbmcgui
import xbmcplugin


class RadioChannelsView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(RadioChannelsView, self).__init__(scene, view_router, "radiochannels", parent_view)
        self.lazy_radios = None

    def set_lazy_radios(self, lazy_radios):
        self.lazy_radios = lazy_radios

    def _get_lazy_radios(self):
        # try to get lazy radios from the parent if none are set
        if self.lazy_radios is None:
            self.lazy_radios = self.parent_view.get_lazy_radios()
        return self.lazy_radios

    def _show_radios(self):
        self.radios = self._get_lazy_radios()()
        list_items = []

        for i in range(0, len(self.radios)):
            try:
                radio = self.radios[i]
                list_item = xbmcgui.ListItem(radio.title, thumbnailImage=radio.picture_big)
                list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
                list_items.append((self.get_url("/%d/tracks" % i), list_item, True))
            except:
                pass
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

    def get_list_items(self):
        self.radios = self._get_lazy_radios()()
        radio = self.radios[self.id]

        list_items = []
        for track in radio.get_tracks():
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

    def show(self):
        self._show_radios()
