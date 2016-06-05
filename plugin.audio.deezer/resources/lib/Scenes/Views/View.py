
class View(object):
	def __init__(self, scene = None, view_router = None, name = "view", parent_view = None):
		self.scene = scene
		self.view_router = view_router
		self.name = name
		self.parent_view = parent_view
		self.child_view = None
		self.id = None

		if self.parent_view is not None:
			self.parent_view.child_view = self

	def set_id(self, id):
		self.id = int(id)

	def get_parent(self):
		return self.parent_view

	def get_child(self):
		return self.child_view

	def get_root(self):
		if self.parent_view == None:
			return self
		else:
			return self.parent_view.get_root()

	def get_path(self):
		return self.scene.scene_router.get_path(self.scene)

	def get_url(self, path = ''):
		url = self.scene.scene_router.get_url(self.scene)
		query = '' if len(url['query']) == 0 else ("?%s" % url['query'])
		return "%s?scene=%s&path=%s%s%s" % (self.scene.scene_router.base_url, self.scene.name, url['path'], path, query)

	#each view can override this method to pass list items to the tracksview
	def get_list_items(self):
		return []

	#each view should override this method
	def show(self):
		pass

	def add_item_track_info(self, item, track):
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

