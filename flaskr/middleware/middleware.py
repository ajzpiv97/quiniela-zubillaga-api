import json
from werkzeug.wrappers import Request, Response


class ContentTypeMiddleware(object):
    def __init__(self, app):  # pragma: no cover
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        headers = request.headers

        if 'Accept' in headers:
            if 'application/json' in headers['Accept']:
                return self.app(environ, start_response)

        if 'Content-Type' in headers:
            if 'application/json' in headers['Content-Type']:
                return self.app(environ, start_response)

        result = json.dumps({'result': 'Requests must contain content-type application/json'})
        res = Response(result, content_type='application/json; charset=utf-8')

        res.headers.add("Access-Control-Allow-Origin", "*")
        res.headers.add('Access-Control-Allow-Headers', "*")
        res.headers.add('Access-Control-Allow-Methods', "*")

        res.status_code = 403

        return res(environ, start_response)
