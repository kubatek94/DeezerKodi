from .TracksView import TracksView
from .AlbumsView import AlbumsView
from .ArtistsView import ArtistsView, ArtistMenuView, ArtistTopView
from .PlaylistsView import PlaylistsView
from .RadioChannelsView import RadioChannelsView
from .ChartView import ChartView
from .SearchView import SearchView


class ViewRouter(object):
    def __init__(self, scene):
        self.scene = scene
        self.root = None

        self.views = {
            "tracks": lambda parent: TracksView(scene=self.scene, view_router=self, parent_view=parent),
            "albums": lambda parent: AlbumsView(scene=self.scene, view_router=self, parent_view=parent),
            "artists": lambda parent: ArtistsView(scene=self.scene, view_router=self, parent_view=parent),
            "playlists": lambda parent: PlaylistsView(scene=self.scene, view_router=self, parent_view=parent),
            "artistmenu": lambda parent: ArtistMenuView(scene=self.scene, view_router=self, parent_view=parent),
            "artisttop": lambda parent: ArtistTopView(scene=self.scene, view_router=self, parent_view=parent),
            "radiochannels": lambda parent: RadioChannelsView(scene=self.scene, view_router=self, parent_view=parent),
            "chart": lambda parent: ChartView(scene=self.scene, view_router=self, parent_view=parent),
            "search": lambda parent: SearchView(scene=self.scene, view_router=self, parent_view=parent)
        }

    # e.g path = /playlists/tracks/1234567
    # e.g path = /albums/123456/tracks
    def route(self, path):
        parts = path.split('/')
        parent = self.root
        for part in parts:
            if part in self.views:
                view = self.views[part]
                parent = view(parent)
                if self.root is None:
                    self.root = parent
            else:
                if parent is not None:
                    parent.set_id(part)
        return parent
