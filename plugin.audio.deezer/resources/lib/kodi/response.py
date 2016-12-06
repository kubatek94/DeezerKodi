import sys
import urlparse
from . import xbmc

class Response(object):
    """
    Response aggregates the output and can display it to the user in a list.
    It may have an action instead, which will for example create a redirect request so that other page will be shown.
    """

    def __init__(self, kernel):
        self._kernel = kernel
        self._output = []

    def show(self):
        pass