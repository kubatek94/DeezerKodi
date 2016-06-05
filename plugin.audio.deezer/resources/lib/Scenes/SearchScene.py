from .Scene import Scene
from ..cache import Cache
from .Views.ViewRouter import ViewRouter


class SearchScene(Scene):
    def __init__(self, scene_router):
        super(SearchScene, self).__init__(scene_router, "search", "Search Scene")

        self.cache = Cache("MySearchScene")

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        self.set_view(view)

        self.cache.save()
