from .Scene import Scene
from ..cache import Cache
from .Views.ChartView import ChartView
from .Views.ViewRouter import ViewRouter

class ChartScene(Scene):
	def __init__(self, sceneRouter):
		super(ChartScene, self).__init__(sceneRouter, "chart", "Chart Scene")
		print "Initialise ChartScene"

		self.cache = Cache("ChartScene")
		self.chart = self.cache.get('chart', defaultProducer = lambda: self.sceneRouter.api.getChart())

		viewRouter = ViewRouter(self)
		view = viewRouter.route(self.sceneRouter.getPath(self))
		viewRouter.root.setLazyChart(lambda:self.chart)
		self.setView(view)

		self.cache.save()