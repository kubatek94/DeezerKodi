from .Scene import Scene
from ..cache import Cache
from .Views.ViewRouter import ViewRouter


class MyAlbumsScene(Scene):
    def __init__(self, scene_router):
        super(MyAlbumsScene, self).__init__(scene_router, "albums", "My Albums Scene")

        self.cache = Cache("MyAlbumsScene")

        self.user = self.scene_router.get_user()
        self.albums = self.cache.get('albums', default_producer=lambda: self.user.get_albums())

        view_router = ViewRouter(self)
        view = view_router.route(self.scene_router.get_path(self))
        view_router.root.set_lazy_albums(lambda: self.albums)
        self.set_view(view)

        self.cache.save()
