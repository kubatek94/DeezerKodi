from .View import View

import os
import xbmc
import xbmcgui
import xbmcplugin

class SearchView(View):
	def __init__(self, scene, view_router, parent_view = None):
		super(SearchView, self).__init__(scene, view_router, "search", parent_view)

	def _get_query(self):
		dialog = xbmcgui.Dialog()
		return dialog.input(self.scene.scene_router.language(self.id))

	def _search(self, query):
		#check if query is in the cache first
		if self.scene.cache.has(query):
			return self.scene.cache.get(query)

		#otherwise do the search
		search = {
			3010 : lambda q: self.scene.scene_router.api.search(query=q),
			3011 : lambda q: self.scene.scene_router.api.search_artist(query=q),
			3012 : lambda q: self.scene.scene_router.api.search_album(query=q),
			3013 : lambda q: self.scene.scene_router.api.search_track(query=q)
		}
		if self.id in search:
			results = search[self.id](query)
			#and put the result in the cache
			self.scene.cache.set(query, results)
			return results
		return None

	def get_lazy_albums(self):
		self.query = ''
		#check if query isn't in the url already
		url_query = self.scene.scene_router.get_query().split("=")
		if "searchQuery" in url_query:
			self.query = url_query[1]
		else:
			self.query = self._get_query()
			self.scene.scene_router.set_query("searchQuery=%s" % self.query)

		if self.query != '':
			results = self._search(self.query)
			return lambda:results
		return lambda:[]

	def get_lazy_artists(self):
		self.query = ''
		#check if query isn't in the url already
		url_query = self.scene.scene_router.get_query().split("=")
		if "searchQuery" in url_query:
			self.query = url_query[1]
		else:
			self.query = self._get_query()
			self.scene.scene_router.set_query("searchQuery=%s" % self.query)

		if self.query != '':
			results = self._search(self.query)
			return lambda:results
		return lambda:[]

	def get_list_items(self):
		self.query = ''
		#check if query isn't in the url already
		url_query = self.scene.scene_router.get_query().split("=")
		if "searchQuery" in url_query:
			self.query = url_query[1]
		else:
			self.query = self._get_query()

		if self.query != '':
			results = self._search(self.query)
			url = self.get_url()

			list_items = []
			for track in results:
				try:
					list_item = xbmcgui.ListItem("%s - %s" % (track.artist.name, track.title), thumbnailImage=track.album.cover_big)
					list_item.setProperty('IsPlayable', 'true')
					list_item.setArt({'fanart': track.artist.picture_big})
					self.add_item_track_info(list_item, track)
					list_items.append((self.get_url("/%d?searchQuery=%s" % (track.id, self.query)), list_item, False))
				except:
					pass
			return list_items
		return []

	#to display menu
	def _show_search_menu(self):
		items = {
			3010 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "search-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/3010/tracks') #search all
			},
			3011 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "myartists-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/3011/artists') #search artist
			},
			3012 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "myalbums-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/3012/albums') #search album
			},
			3013 : {
				"image" : xbmc.translatePath(os.path.join(self.scene.scene_router.images_path, "search-%s.png" % self.scene.scene_router.color)),
				"url" : self.get_url('/3013/tracks') #search track
			}
		}
		list_items = []
		for item in items:
			list_item = xbmcgui.ListItem(self.scene.scene_router.language(item), iconImage=items[item]["image"])
			list_item.setArt({'fanart': self.scene.scene_router.fanart_path})
			list_items.append((items[item]["url"], list_item, True))
		xbmcplugin.addDirectoryItems(self.scene.scene_router.addon_handle, list_items)

	def show(self):
		self._show_search_menu()
			