try:
    import xbmc
except:
    import mock.xbmc as xbmc

try:
    import xbmcgui
except:
    import mock.xbmcgui as xbmcgui

try:
    import xbmcaddon
except:
    import mock.xbmcaddon as xbmcaddon


try:
    import xbmcplugin
except:
    import mock.xbmcplugin as xbmcplugin