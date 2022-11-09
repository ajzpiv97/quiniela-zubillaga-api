import unittest

import json

from flaskr.app import create_app
from flaskr.db.users import Users
from flaskr.utils.extensions import db, bcrypt


class AuthTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    app = create_app()

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.client = cls.app.test_client

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            password_hash = bcrypt.generate_password_hash('1234')

            new_user = Users(email='test@gmail.com',
                             name='Test', last_name='Test',
                             password=password_hash)

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
        self.assertEqual(201, res.status_code)
        self.assertEqual('Usuario fue creado exitosamente', data['message'])

    def test2_duplicate_user(self):
        header_obj = {
            "Content-Type": 'application/json'
        }
        data = {"email": "test@gmail.com",
                "name": "Test1",
                "lastName": "test", "password": "1234"}
        res = self.client().post('/auth/register',
                                 json=data, headers=header_obj)
        self.assertEqual(400, res.status_code)

    def test3_user_login(self):
        header_obj = {
            "Content-Type": 'application/json'
        }
        data = {"email": "test@gmail.com",
                "password": "1234"}
        res = self.client().post('/auth/login',
                                 json=data, headers=header_obj)
        self.assertEqual(200, res.status_code, )

    def test4_fail_user_login_user_does_not_exist(self):
        header_obj = {
            "Content-Type": 'application/json'
        }
        data = {"email": "test123@gmail.com",
                "password": "1234"}
        res = self.client().post('/auth/login',
                                 json=data, headers=header_obj)
        self.assertEqual(400, res.status_code,)

    def test5_fail_user_login_wrong_password(self):
        header_obj = {
            "Content-Type": 'application/json'
        }
        data = {"email": "test@gmail.com",
                "password": "123"}
        res = self.client().post('/auth/login',
                                 json=data, headers=header_obj)
        self.assertEqual(401, res.status_code)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()
