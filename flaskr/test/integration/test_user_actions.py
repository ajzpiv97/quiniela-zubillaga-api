import unittest
from datetime import datetime
from flaskr.app import create_app
from flaskr.db.games import Games
from flaskr.db.users import Users
from flaskr.utils.extensions import db, bcrypt
from flaskr.utils.jwt_generation import generate_jwt


class UserActionsTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    game2 = None
    game1 = None
    user_data = None
    app = create_app()

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.client = cls.app.test_client

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            password_hash = bcrypt.generate_password_hash('1234')
            cls.user_data = {"email": 'test@gmail.com',
                             "name": 'Test', "last_name": 'File',
                             "password": password_hash}
            new_user = Users(**cls.user_data)
            new_user.create()

            cls.game1 = Games(team_a='team_a', team_b='team_b', score='1-1', date=datetime.utcnow())
            cls.game2 = Games(team_a='team_c', team_b='team_d', score='2-1', date=datetime.utcnow())

            cls.game1.create()
            cls.game2.create()

    def test1_new_predictions(self):
        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 1, 'score2': 2},
                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 0}]}

        res = self.client().post('/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(201, res.status_code)

    def test2_update_predictions(self):
        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 1, 'score2': 2},
                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 0}]}

        self.client().post('/user-actions/update-predictions',
                           json=data, headers=header_obj)

        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 3, 'score2': 1},
                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 1}]}

        res = self.client().post('/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(201, res.status_code)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()
