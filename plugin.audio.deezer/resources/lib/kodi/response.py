from . import xbmcgui, xbmcplugin

class Response(object):
    """
    Response aggregates the output and can display it to the user in a list.
    It may have an action instead, which will for example create a redirect request so that other page will be shown.

    @type _kernel: kernel.Kernel
    @type _controller: controller.Controller
    @type _output: list
    """

    def __init__(self, kernel, controller=None):
        self._kernel = kernel
        self._controller = controller
        self._output = []

    def show(self):
        """@rtype: bool"""
        return False


class NotFoundResponse(Response):
    """@type _url: str"""

    def __init__(self, kernel, url):
        Response.__init__(self, kernel)
        self._url = url

    def show(self):
        utils = self._kernel.get_utils()
        utils.notify("404", "Route not found for " + self._url)
        return False


class DefaultResponse(Response):
    def __init__(self, kernel, controller, items):
        Response.__init__(self, kernel, controller)
        self._items = items

    def show(self):
        xbmcplugin.addDirectoryItems(self._controller.get_request().get_id(), [(item.url, item.to_list_item(), True) for item in self._items])
        return True

class ErrorResponse(Response):
    """@type _error: BaseException"""

    def __init__(self, kernel, error):
        Response.__init__(self, kernel)
        self._error = error

    def show(self):
        utils = self._kernel.get_utils()
        utils.notify("Error", "%s" % self._error)
        return False


class Item(object):

    def __init__(self, label, url, label2=None, icon=None, thumbnail=None, fanart=None):
        self.label = label
        self.label2 = label2
        self.url = url
        self.icon = icon
        self.thumbnail = thumbnail
        self.fanart = fanart

    def to_list_item(self):
        list_item = xbmcgui.ListItem(self.label, path=self.url)
        list_item.setArt({'fanart': self.fanart})
        list_item.setArt({'icon': self.icon})
        list_item.setArt({'thumbnail': self.thumbnail})
        return list_item