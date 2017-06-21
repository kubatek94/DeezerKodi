import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources'))

from kodi.plugin import AppPlugin
from kodi.request import Request
from kodi.config import AppConfigLoader
import resources

#create the app
app = AppPlugin()

#load config from each bundle declared in resources.bundles and combine each config into one
config_loader = AppConfigLoader(app)
config, bundles = config_loader.load_config(resources)

#set the config, register bundles, perform any caching of service container and the config
app.boot(config, bundles)

#handle the request
request = Request.create_from_globals()
response = app.handle(request)

#show the response on the screen or something totally different
response.send()

#execute final action before we quit
app.terminate(request, response)