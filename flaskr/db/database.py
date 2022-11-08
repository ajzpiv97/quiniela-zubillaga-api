from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app: Flask, database_path: str) -> SQLAlchemy:
    """

    :param app:
    :param database_path:
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    return db
