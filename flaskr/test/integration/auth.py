import os
import unittest

import json

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from flaskr.db.database import setup_db
from flaskr.db.users import Users


class AuthTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    db: SQLAlchemy
    app = create_app()

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        database_path = os.environ.get('DATABASE_URL')
        assert database_path is not None, 'Set DATABASE_URL!'
        cls.db = setup_db(cls.app, database_path)
        cls.client = cls.app.test_client

        with cls.app.app_context():
            cls.db.drop_all()
            cls.db.create_all()
            new_user = Users(email='test@gmail.com',
                             name='Test', last_name='Test',
                             password='1234')

            new_user.insert()

    def test1_create_new_user(self):
        header_obj = {
            "Content-Type": 'application/json'
        }
        data = {"email": "test@hotmail.com",
                "name": "Test1",
                "lastName": "test", "password": "1234"}
        res = self.client().post('/auth/register',
                                 json=data, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual('Usuario fue creado exitosamente', data['message'])

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            cls.db.drop_all()
