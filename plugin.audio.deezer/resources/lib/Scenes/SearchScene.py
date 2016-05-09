from .Scene import Scene
from ..cache import Cache
from .Views.SearchView import SearchView
from .Views.ViewRouter import ViewRouter

class SearchScene(Scene):
	def __init__(self, sceneRouter):
		super(SearchScene, self).__init__(sceneRouter, "search", "Search Scene")
		print "Initialise SearchScene"

		self.cache = Cache("MySearchScene")

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		self.setView(view)

		self.cache.save()