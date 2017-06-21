from .Scene import Scene
from ..cache import Cache
from .Views.ViewRouter import ViewRouter


class MyPlaylistsScene(Scene):
    def __init__(self, scene_router):
        super(MyPlaylistsScene, self).__init__(scene_router, "playlists", "My Playlists Scene")

        self.cache = Cache("MyPlaylistsScene")

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_playlists(lambda: self.cache.get('playlists', default_producer=lambda: self.scene_router.get_user().get_playlists()))
        self.set_view(view)

        self.cache.save()
