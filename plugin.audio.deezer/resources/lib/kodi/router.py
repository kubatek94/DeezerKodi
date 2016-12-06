import re
_rule_re = re.compile(r'(?P<static>[^<]*)<?(?P<variable>[a-zA-Z_]*)>?')


class RuleNotFoundError(Exception):
    pass


class Router(object):
    def __init__(self, kernel):
        self._kernel = kernel
        self._config = self._kernel.get_config('router')
        self.rules = [] if 'rules' not in self._config else self._config['rules']

    def add_rule(self, rule, target, cls=None):
        name = (cls if cls else target.__module__.split('.')[-1]) + ':' + target.__name__

        self.rules.append({
            'regex' : None,
            'rule' : rule,
            'target' : name,
            'module': target.__module__,
        })

    def match(self, url):
        for rule in self.rules:
            if rule['regex'] is None:
                rule['regex'] = Router.compile_rule(rule['rule'])
            elif isinstance(rule['regex'], basestring):
                rule['regex'] = re.compile(rule['regex'])
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
                regex.append('(?P<%s>[^/]+?)' % var)
        return re.compile(r'^%s$' % (''.join(regex)))

    def route(self, rule, name):
        def route_decorator(f):
            self.add_rule(rule, target=f)
            def f_wrapper(*args, **kwargs):
                return f(args, kwargs)
            return f_wrapper
        return route_decorator