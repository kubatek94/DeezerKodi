from ..kodi.compiler import compile
from ..kodi.response import Response

class Settings(object):
    def __init__(self, kernel):
        self.kernel = kernel

    @compile('/', 'Settings')
    @compile('/<user>', 'Settings')
    def show_settings(self, user='me'):
        print user
        return Response(self)