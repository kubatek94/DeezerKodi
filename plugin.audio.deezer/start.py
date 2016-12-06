from resources.lib.kodi.kernel import Kernel
from resources.lib.kodi.request import Request
from config import config
import sys

kernel = Kernel(config)

if config['plugin']['env'] == 'dev':
    sys.argv = ['plugin://' + config['plugin']['name'] + '/kubatek94', 0, '']

request = Request.create_from_globals()
response = kernel.handle(request)

response.show()
kernel.terminate(request, response)