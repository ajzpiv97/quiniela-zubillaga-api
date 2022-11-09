import logging
import os
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime as dt
from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.routes import auth
from flaskr.utils.custom_response import CustomResponseHandler
from flaskr.utils.error_handler import error_handler

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': "[%(asctime)s] [p%(process)s] [%(levelname)s] {%(filename)s:"
                  "%(lineno)d} %(message)s",
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__, instance_relative_config=True)


def create_app():
    testing = os.environ.get('TESTING', False)
    app.config['TESTING'] = testing
    app.response_class = CustomResponseHandler

    app.register_blueprint(auth.bp)
    app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)
    CORS(app, resources=r'/*')
    error_handler(app)

    # CORS Headers
    @app.after_request
    def after_request(response: Flask.response_class):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.after_request
    def log_after_request(response):
        app.logger.info(
            "path: %s | method: %s | status: %s",
            request.path,
            request.method,
            response.status
        )

        return response

    return app
