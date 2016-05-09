from .Scene import Scene
from ..cache import Cache
from .Views.PlaylistsView import PlaylistsView
from .Views.ViewRouter import ViewRouter

class MyPlaylistsScene(Scene):
	def __init__(self, sceneRouter):
		super(MyPlaylistsScene, self).__init__(sceneRouter, "playlists", "My Playlists Scene")
		print "Initialise MyPlaylistsScene"

		self.cache = Cache("MyPlaylistsScene")

		self.user = self.sceneRouter.getUser()
		self.playlists = self.cache.get('playlists', defaultProducer = lambda: self.user.getPlaylists())

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		viewRouter.root.setLazyPlaylists(lambda:self.playlists)
		self.setView(view)

		self.cache.save()