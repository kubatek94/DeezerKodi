class Scene(object):
    def __init__(self, scene_router, name="scene", title="Scene"):
        self.scene_router = scene_router
        self.name = name
        self.title = title

    def set_view(self, view):
        self.view = view
        self.view.show()

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()
