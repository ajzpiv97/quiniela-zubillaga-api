import uuid

from sqlalchemy import Column, Integer, String

from flaskr.db.base_model import BaseModel
from flaskr.db.database import db


class Users(db.Model):
    __tablename__ = 'tbl_users'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    total_points = Column(Integer, default=None, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


