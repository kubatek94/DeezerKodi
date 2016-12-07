#This file will compile the routes and store them before packaging, which will be more efficient than compiling them at runtime
#It will also look for all the dependency injections and create a service container configuration
import sys
from os import walk

from resources.lib.kodi.kernel import Kernel
from resources.lib.kodi.router import Router
from resources.lib.kodi import compiler

class ConfigCompiler(object):
    def __init__(self, name):
        self.name = name
        self.config = {}

    def compile(self):
        return self.config


#router needs to import all app classes, which will cause them to execute the decorators
#and effectively add the rules to the router object inside kodi.compiler
#we can then compile the rules and return them
class RouterCompiler(ConfigCompiler):
    def compile(self):
        config = {
            'plugin': {
                'env': 'compiler'
            },
            'service_container': {},
            'router': {}
        }

        kernel = Kernel(config)
        router = Router(kernel)

        def route_compile(rule, cls=None):
            def compile_decorator(f):
                router.add_rule(rule, target=f, cls=cls)
                return f
            return compile_decorator

        compiler.compile = route_compile

        for (dirpath, dirnames, filenames) in walk('resources/lib/app/'):
            for file in filenames:
                if file.endswith('.py'):
                    __import__('resources.lib.app.' + file.replace('/', '.')[:-3])
        for rule in router.rules:
            rule['regex'] = Router.compile_rule(rule['rule']).pattern
        return {'rules': router.rules}


class ServiceContainerCompiler(ConfigCompiler):
    def compile(self):
        return {}

class PluginCompiler(ConfigCompiler):
    def compile(self):
        return {'name': sys.argv[1], 'env': sys.argv[2]}

class CompilerAggregator(ConfigCompiler):
    def __init__(self, name):
        ConfigCompiler.__init__(self, name)
        self._compilers = []

    def add(self, compiler):
        self._compilers.append(compiler)

    def compile(self):
        for compiler in self._compilers:
            self.config[compiler.name] = compiler.compile()
        return "%s = %s" % (self.name, self.config)


all = CompilerAggregator('config')
all.add(PluginCompiler('plugin'))
all.add(ServiceContainerCompiler('service_container'))
all.add(RouterCompiler('router'))
with open('config.py', 'w') as cfg:
    cfg.write(all.compile())