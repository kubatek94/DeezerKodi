from .Scene import Scene
from ..cache import Cache
from .Views.AlbumsView import AlbumsView
from .Views.ViewRouter import ViewRouter

class MyAlbumsScene(Scene):
	def __init__(self, sceneRouter):
		super(MyAlbumsScene, self).__init__(sceneRouter, "albums", "My Albums Scene")
		print "Initialise MyAlbumsScene"

		self.cache = Cache("MyAlbumsScene")

		self.user = self.sceneRouter.getUser()
		self.albums = self.cache.get('albums', defaultProducer = lambda: self.user.getAlbums())

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		viewRouter.root.setLazyAlbums(lambda:self.albums)
		self.setView(view)

		self.cache.save()