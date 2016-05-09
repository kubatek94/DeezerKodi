
class View(object):
	def __init__(self, scene = None, viewRouter = None, name = "view", parentView = None):
		self.scene = scene
		self.viewRouter = viewRouter
		self.name = name
		self.parentView = parentView
		self.childView = None
		self.id = None

		if self.parentView is not None:
			self.parentView.childView = self

	def setID(self, id):
		self.id = int(id)

	def getParent(self):
		return self.parentView

	def getChild(self):
		return self.childView

	def getRoot(self):
		if self.parentView == None:
			return self
		else:
			return self.parentView.getRoot()

	def getPath(self):
		return self.scene.sceneRouter.getPath(self.scene)

	def getUrl(self, path = ''):
		url = self.scene.sceneRouter.getUrl(self.scene)
		query = '' if len(url['query']) == 0 else ("?%s" % url['query'])
		return "%s?scene=%s&path=%s%s%s" % (self.scene.sceneRouter.baseUrl, self.scene.name, url['path'], path, query)

	#each view can override this method to pass list items to the tracksview
	def getListItems(self):
		return []

	#each view should override this method
	def show(self):
		pass

	def addItemTrackInfo(self, item, track):
		try:
			item.setInfo('music', {'tracknumber' : track.track_position})
		except:
			pass
		try:
			item.setInfo('music', {'discnumber' : track.disk_number})
		except:
			pass
		try:
			item.setInfo('music', {'duration' : track.duration})
		except:
			pass
		try:
			item.setInfo('music', {'album' : track.album.title})
		except:
			pass
		try:
			item.setInfo('music', {'artist' : track.artist.name})
		except:
			pass
		try:
			item.setInfo('music', {'title' : track.title})
		except:
			pass

