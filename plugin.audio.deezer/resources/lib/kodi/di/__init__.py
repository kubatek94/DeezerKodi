class ServiceMissingError(Exception):
    pass


class ServiceContainer(object):
    def __init__(self, kernel):
        self._kernel = kernel
        self._config = self._kernel.get_config('service_container')
        self._services = {} if 'services' not in self._config else self._config['services']

    def put(self, name, stuff):
        self._services[name] = stuff

    def get(self, name):
        return self._services[name]

    def has(self, name):
        return name in self._services

    def inject(self, *args, **kwargs):
        def _inject(f):
            for key, name in kwargs.items():
                setattr(f, key, ServiceProvider(self, f, name))
            return f
        return _inject


class ServiceProvider(object):
    def __init__(self, service_container, f, name):
        self.service_container = service_container
        self.f = f
        self.name = name
        self.got = False

    def __get__(self, instance, owner):
        if not self.got:
            self.got = True
            return None

        if self.service_container.has(self.name):
            i = self.service_container.get(self.name)()
            setattr(instance, self.name, i)
            return i
        else:
            raise ServiceMissingError("Dependency '%s' required by %s was not provided!" % (self.name, str(instance)))