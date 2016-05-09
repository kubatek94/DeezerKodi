from .Scene import Scene
from ..cache import Cache
from .Views.RadioChannelsView import RadioChannelsView
from .Views.ViewRouter import ViewRouter

class RadioChannelsScene(Scene):
	def __init__(self, sceneRouter):
		super(RadioChannelsScene, self).__init__(sceneRouter, "radiochannels", "Radio Channels Scene")
		print "Initialise RadioChannelsScene"

		self.cache = Cache("RadioChannelsScene")
		self.radios = self.cache.get('radios', defaultProducer = lambda: self.sceneRouter.api.getRadios())

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		viewRouter.root.setLazyRadios(lambda:self.radios)
		self.setView(view)

		self.cache.save()