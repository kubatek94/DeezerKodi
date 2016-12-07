from . import xbmc

def addDirectoryItems(handle, items, totalItems=None):
    totalItems = totalItems if totalItems is not None else len(items)
    xbmc.log('Add %d items' % totalItems)

def endOfDirectory(handle, succeeded=True):
    xbmc.log('End of directory => %s' % succeeded)