from .Scene import Scene
import os
import xbmc
import xbmcgui
import xbmcplugin

class MainScene(Scene):
	def __init__(self, sceneRouter):
		super(MainScene, self).__init__(sceneRouter, "main", "Main Scene")
		print "Initialise MainScene"
		self.color = "white"
		self._makeScene()

	def _makeScene(self):
		items = {
			2000 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "chart-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "chart")
			},
			2001 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "radiochannels-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "radiochannels")
			},
			2002 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "myplaylists-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "playlists")
			},
			2003 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "myalbums-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "albums")
			},
			2004 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "myartists-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "artists")
			},
			2005 : {
				"image" : xbmc.translatePath(os.path.join(self.sceneRouter.imagesPath, "search-%s.png" % self.color)),
				"url" : "%s?scene=%s" % (self.sceneRouter.baseUrl, "search")
			}
		}

		listItems = []

		for item in items:
			listItem = xbmcgui.ListItem(self.sceneRouter.language(item), iconImage=items[item]["image"], thumbnailImage="")
			listItem.setArt({'fanart': self.sceneRouter.fanartPath})
			listItems.append((items[item]["url"], listItem, True))

		xbmcplugin.addDirectoryItems(self.sceneRouter.addonHandle, listItems)