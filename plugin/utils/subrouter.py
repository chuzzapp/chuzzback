from collections import namedtuple
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from .handler_helper import http_exception_to_json_response


Subroute = namedtuple('Subroute', 'pattern, method, handler')


class Subrouter():
    def __init__(self, subroutes):
        self.route_map = Map([
            Rule(x.pattern, methods=[x.method], endpoint=x.handler.__name__)
            for x in subroutes
        ])

        self.methods = list(set([x.method for x in subroutes]))

        self.handlers = dict([
            (x.handler.__name__, x.handler)
            for x in subroutes
        ])

    def dispatch(self, request):
        urls = self.route_map.bind_to_environ(request.environ)
        try:
            endpoint, args = urls.match()
            return self.handlers[endpoint](request, **args)
        except HTTPException as e:
            return http_exception_to_json_response(e)
