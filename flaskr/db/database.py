from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr.utils.utils import modify_database_url_to_add_dialect

db = SQLAlchemy()


def setup_db(app: Flask, database_path: str) -> SQLAlchemy:
    """

    :param app:
    :param database_path:
    """

    db.app = app
    db.init_app(app)

    return db
