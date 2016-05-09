from .Scene import Scene
from ..cache import Cache
from .Views.ArtistsView import ArtistsView
from .Views.ViewRouter import ViewRouter

class MyArtistsScene(Scene):
	def __init__(self, sceneRouter):
		super(MyArtistsScene, self).__init__(sceneRouter, "artists", "My Artists Scene")
		print "Initialise MyArtistsScene"

		self.cache = Cache("MyArtistsScene")

		self.user = self.sceneRouter.getUser()
		self.artists = self.cache.get('artists', defaultProducer = lambda: self.user.getArtists())

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		viewRouter.root.setLazyArtists(lambda:self.artists)
		self.setView(view)

		self.cache.save()