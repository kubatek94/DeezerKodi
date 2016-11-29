import sys
import urlparse

class Request(object):

    def __init__(self, url, args):
        self.url = url
        self.args = args

    @classmethod
    def create_from_globals(cls):
        return Request(sys.argv[0], urlparse.parse_qs(sys.argv[2][1:]))

    # url consists of the path and query parts
    def get_url(self, scene=None):
        return {'path': self.get_path(scene), 'query': self.get_query(scene)}


    def set_url(self, url):
        full_url = "%s?%s" % (url['path'], url['query'])
        self.args['path'] = [full_url]


    # path consists of e.g. /search/3000/tracks/1
    def get_path(self, scene=None):
        path = None
        if scene is None:
            path = self.args.get('path', ["/"])[0]
        else:
            path = self.args.get('path', ["/%s" % scene.name])[0]
        return path.split('?')[0]


    def set_path(self, path):
        url = {'path': path, 'query': self.get_query()}
        self.set_url(url)


    def set_query(self, query):
        url = {'path': self.get_path(), 'query': query}
        self.set_url(url)


    # query consists of e.g. searchQuery=Hello&foo=bar
    def get_query(self, scene=None):
        path = None
        if scene is None:
            path = self.args.get('path', ["/"])[0]
        else:
            path = self.args.get('path', ["/%s" % scene.name])[0]
        s = path.split('?')
        if len(s) > 1:
            return s[1]
        else:
            return ''