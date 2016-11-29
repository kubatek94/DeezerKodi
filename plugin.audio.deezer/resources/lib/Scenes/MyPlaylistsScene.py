from .Scene import Scene
from ..kodi.cache import Cache
from .Views.ViewRouter import ViewRouter


class MyPlaylistsScene(Scene):
    def __init__(self, scene_router):
        super(MyPlaylistsScene, self).__init__(scene_router, "playlists", "My Playlists Scene")

        self.cache = Cache("MyPlaylistsScene")

        self.user = self.scene_router.get_user()
        self.playlists = self.cache.get('playlists', default_producer=lambda: self.user.get_playlists())

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_playlists(lambda: self.playlists)
        self.set_view(view)

        self.cache.save()
