import os
from flask import Flask
from flask_cors import CORS

from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.routes import auth

app = Flask(__name__, instance_relative_config=True)


def create_app():

    testing = os.environ.get('TESTING', False)
    app.config['TESTING'] = testing
    app.register_blueprint(auth.bp)
    app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)
    CORS(app, resources=r'/*')

    return app
