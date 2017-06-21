from .Scene import Scene
from ..cache import Cache
from .Views.ViewRouter import ViewRouter


class ChartScene(Scene):
    def __init__(self, scene_router):
        super(ChartScene, self).__init__(scene_router, "chart", "Chart Scene")

        self.cache = Cache("ChartScene")

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_chart(lambda: self.cache.get('chart', default_producer=self.scene_router.api.get_chart))
        self.set_view(view)

        self.cache.save()
