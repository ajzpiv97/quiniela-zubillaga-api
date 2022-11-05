from flask import Flask
from flask_cors import CORS

from flaskr.db.database import db
from flaskr.middleware.middleware import ContentTypeMiddleware
from flaskr.views import auth

app = Flask(__name__, instance_relative_config=True)

app.register_blueprint(auth.bp)

app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)
CORS(app, resources=r'/*')
url = ''
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
with app.app_context():
    db.create_all()
