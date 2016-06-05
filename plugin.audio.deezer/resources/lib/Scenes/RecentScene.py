from .Scene import Scene
from .Views.ViewRouter import ViewRouter

class RecentScene(Scene):
    def __init__(self, scene_router):
        super(RecentScene, self).__init__(scene_router, "recent", "Recent Scene")

        # we wont use cache for this scene, as it should reflect most recent state
        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self) + "/tracks")
        view_router.root.set_lazy_tracks(lambda: self.scene_router.get_user().get_history())
        self.set_view(view)