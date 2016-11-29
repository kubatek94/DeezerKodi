class UserManager(object):
    _user = None
    onChange = [] #users can add callbacks here to be notified whenever a different user has been selected

    def __init__(self, scene_router):
        self._scene_router = scene_router

    def sign_in(self, username, password):
        self._scene_router

    def is_signed_in(self):
        return self._user is not None

    def get_current(self):
        return self._user