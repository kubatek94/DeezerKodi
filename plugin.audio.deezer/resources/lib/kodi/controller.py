from di import ServiceMissingError
from response import DefaultResponse

class Controller(object):
    """
    @type _kernel: kernel.Kernel
    @type _request: request.Request
    """

    def __init__(self, kernel, request):
        self._kernel = kernel
        self._request = request

    def get_request(self):
        return self._request

    def get(self, service_name):
        """
        @type service_name: str
        """
        container = self._kernel.get_service_container()
        if not container.has(service_name):
            raise ServiceMissingError("Service '%s' not found" % service_name)
        return container.get(service_name)

    def to_response(self, items):
        """@type items: list[response.Item]"""
        return DefaultResponse(self._kernel, self, items)