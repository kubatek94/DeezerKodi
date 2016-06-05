from .View import View

import os
import xbmc
import xbmcgui
import xbmcplugin

class ChartView(View):
	def __init__(self, scene, view_router, parent_view = None):
		super(ChartView, self).__init__(scene, view_router, "chart", parent_view)
		self.lazy_chart = None

	def set_lazy_chart(self, lazy_chart):
		self.lazy_chart = lazy_chart

	def _get_lazy_chart(self):
		#try to get lazy chart from the parent if none are set
		if self.lazy_chart is None:
			self.lazy_chart = self.parent_view.get_lazy_chart()
		return self.lazy_chart

	#to display the albums
	def get_lazy_albums(self):
		chart = self._get_lazy_chart()()
		return lambda:chart.get_albums()

	#to display the artists
	def get_lazy_artists(self):
		chart = self._get_lazy_chart()()
		return lambda:chart.get_artists()

	#to display the playlists
	def get_lazy_playlists(self):
		chart = self._get_lazy_chart()()
		return lambda:chart.get_playlists()

	#to display the tracks
	def get_list_items(self):
		chart = self._get_lazy_chart()()
		list_items = []
		for track in chart.get_tracks():
			try:
				list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
				list_item.setProperty('IsPlayable', 'true')
				list_item.setArt({'fanart': track.artist.picture_big})
				self.add_item_track_info(list_item, track)
				list_items.append((self.get_url("/%d" % track.id), list_item, False))
			except:
				pass
		return list_items

	#to diplay first menu
	def _show_chart_menu(self):
		items = {
			3005 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "genre-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/tracks')
			},
			3006 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "myalbums-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/albums')
			},
			3007 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "myartists-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/artists')
			},
			3008 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "myplaylists-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/playlists')
			}
		}
		list_items = []
		for item in items:
			list_item = xbmcgui.ListItem(self.scene.scene_router.language(item), iconImage=items[item]["image"])
			list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
			list_items.append((items[item]["url"], list_item, True))
		xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

	def show(self):
		self._show_chart_menu()