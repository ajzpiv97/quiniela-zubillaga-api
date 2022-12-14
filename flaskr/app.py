import logging
from flask import Flask, request
from flask_cors import CORS
from sys import platform

from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.utils.error_handler import error_handler
from flaskr.utils.extensions import bcrypt, db, migrate
from flaskr.utils.env_variables import SETTING
from flaskr.utils.commands import migrate as migration, populate, init_games, update_game_time, init_rounds


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
    register_commands(app)
    return app


def setup_configs(app):
    app.config.from_object(f'flaskr.utils.config.{SETTING.lower().capitalize()}Config')


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    from flaskr.routes import auth, status, user_actions
    app.register_blueprint(auth.bp)
    app.register_blueprint(status.bp)
    app.register_blueprint(user_actions.bp)


def register_error_handlers(app):
    """Register error handlers."""
    error_handler(app)


def configure_logger(app):
    """Configure loggers."""
    logger_type = 'gunicorn.error'
    if platform == 'win32':
        logger_type = 'waitress'
    logger = logging.getLogger(logger_type)
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)


def register_middleware(app):
    app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(migration, app)
    app.cli.add_command(populate)
    app.cli.add_command(init_games)
    app.cli.add_command(update_game_time)
    app.cli.add_command(init_rounds)
