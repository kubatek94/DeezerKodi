from .Scene import Scene
from ..kodi.cache import Cache
from .Views.ViewRouter import ViewRouter


class MyArtistsScene(Scene):
    def __init__(self, scene_router):
        super(MyArtistsScene, self).__init__(scene_router, "artists", "My Artists Scene")

        self.cache = Cache("MyArtistsScene")

        self.user = self.scene_router.get_user()
        self.artists = self.cache.get('artists', default_producer=lambda: self.user.get_artists())

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_artists(lambda: self.artists)
        self.set_view(view)

        self.cache.save()
