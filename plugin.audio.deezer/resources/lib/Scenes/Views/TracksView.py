from .View import View

import xbmcgui
import xbmcplugin


class TracksView(View):
    def __init__(self, scene, view_router, parent_view=None):
        super(TracksView, self).__init__(scene, view_router, "tracks", parent_view)

    def _play_track(self):
        url = self.scene.scene_router.api.get_streaming_url(id=self.id, type='track')
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(self.scene.scene_router.addon_handle, True, listitem=item)

    def _show_tracks(self):
        list_items = self.parent_view.get_list_items()
        xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items, len(list_items))
        xbmcplugin.setContent(self.scene.scene_router.addon_handle, 'songs')

    def show(self):
        if self.id is not None:
            self._play_track()
        else:
            self._show_tracks()
