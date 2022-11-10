import logging
import os
from flask import Flask, request
from flask_cors import CORS
from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.utils.error_handler import error_handler
from flaskr.utils.extensions import bcrypt, db, migrate
from flaskr.utils.utils import modify_database_url_to_add_dialect


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    """
    app = Flask(__name__.split(".")[0])
    setup_configs(app)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    configure_logger(app)
    register_middleware(app)
    return app


def setup_configs(app):
    app.config['TESTING'] = os.environ.get('TESTING', False)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
    app.config["SQLALCHEMY_DATABASE_URI"] = modify_database_url_to_add_dialect(os.environ.get('DATABASE_URL', ''))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    from flaskr.routes import auth, status
    app.register_blueprint(auth.bp)
    app.register_blueprint(status.bp)


def register_error_handlers(app):
    """Register error handlers."""
    error_handler(app)


def configure_logger(app):
    """Configure loggers."""
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def register_middleware(app):
    app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)
    CORS(app, resources=r'/*')

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
