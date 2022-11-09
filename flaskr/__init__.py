import logging
import os
from flask import Flask, request
from flask_cors import CORS
from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.routes import auth, status
from flaskr.utils.error_handler import error_handler


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.config['TESTING'] = os.environ.get('TESTING', False)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
    app.register_blueprint(auth.bp)
    app.register_blueprint(status.bp)
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
