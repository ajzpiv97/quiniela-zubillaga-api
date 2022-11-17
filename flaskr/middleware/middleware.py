import json
from typing import Dict

from flask import Flask
from werkzeug.wrappers import Request, Response


class ContentTypeMiddleware(object):
    def __init__(self, app: Flask.wsgi_app):  # pragma: no cover
        self.app = app

    def __call__(self, environ: Dict, start_response):
        request = Request(environ)
        headers = request.headers

        if request.method == 'OPTIONS':
            return self.app(environ, start_response)

        if 'Accept' in headers:
            if 'application/json' in headers['Accept']:
                return self.app(environ, start_response)

        if 'Content-Type' in headers:
            if 'application/json' in headers['Content-Type']:
                return self.app(environ, start_response)

        result = json.dumps({'result': 'Requests must contain content-type application/json'})
        response = Response(result, content_type='application/json; charset=utf-8')

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")

        response.status_code = 403

        return response(environ, start_response)
