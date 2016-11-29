import re
from . import rules as default_rules

_rule_re = re.compile(r'(?P<static>[^<]*)<?(?P<variable>[a-zA-Z_]*)>?')


class RuleNotFoundError(Exception):
    pass


class Router(object):
    def __init__(self):
        self.rules = default_rules

    def add_rule(self, rule, target):
        self.rules.append({
            'regex' : None,
            'rule' : rule,
            'target' : target
        })

    def match(self, url):
        for rule in self.rules:
            if rule['regex'] is None:
                rule['regex'] = Router.compile_rule(rule['rule'])
            match = rule['regex'].search(url)
            if match is not None:
                kwargs = match.groupdict()
                return (rule, kwargs)
        raise RuleNotFoundError("No rule for url: %s" % url)

    @staticmethod
    def compile_rule(rule):
        regex = []
        for m in _rule_re.finditer(rule):
            static = m.group('static')
            if static:
                regex.append(re.escape(static))
            var = m.group('variable')
            if var:
                regex.append('(?P<%s>[^/]*?)' % var)
        return re.compile(r'^%s$' % (''.join(regex)))


router = Router()

def route(rule, name):
    def route_decorator(func):
        router.add_rule(rule, target=func)
        def func_wrapper(*args, **kw):
           print args
           print kw
        return func_wrapper
    return route_decorator
