from flaskr.app import create_app
from flaskr.utils.extensions import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
