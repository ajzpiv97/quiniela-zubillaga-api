import os

from app import create_app
from flaskr.db.database import setup_db

app = create_app()

database_path = os.environ.get('DATABASE_URL', None)
if database_path is None:
    raise ValueError('DATABASE_URL not set!')

db = setup_db(app, database_path)

with app.app_context():
    db.create_all()
