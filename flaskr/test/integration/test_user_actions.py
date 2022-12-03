import time
import unittest
import uuid

from deepdiff import DeepDiff
from datetime import datetime
from flaskr.app import create_app
from flaskr.db.games import Games
from flaskr.db.predictions import Predictions
from flaskr.db.rounds import Rounds
from flaskr.db.users import Users
from flaskr.utils.extensions import db, bcrypt
from flaskr.utils.jwt_generation import generate_jwt


class UserActionsTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    user_data = None
    user_data1 = None
    app = create_app()

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        cls.client = cls.app.test_client

    def setUp(self) -> None:

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            password_hash = bcrypt.generate_password_hash('1234')
            self.user_data = {"email": 'test@gmail.com',
                              "name": 'Test', "last_name": 'File',
                              "password": password_hash,
                              }
            new_user = Users(**self.user_data)
            new_user.create()

            self.user_data1 = {"email": 'test2@gmail.com',
                               "name": 'Sample', "last_name": 'File',
                               "password": password_hash}
            new_user = Users(**self.user_data1)
            new_user.create()

            round1 = Rounds(id=1, round_name="round1", round_start_datetime='2022-01-01 00:00:00',
                            round_start_timestamp=datetime.utcnow().timestamp(),
                            round_end_datetime='2022-01-02 00:00:00',
                            round_end_timestamp=datetime.utcnow().timestamp()
                            )
            round1.save()

            round2 = Rounds(id=2, round_name="round2", round_start_datetime='2022-01-01 00:00:00',
                            round_start_timestamp=datetime.utcnow().timestamp(),
                            round_end_datetime='2022-01-02 00:00:00',
                            round_end_timestamp=datetime.utcnow().timestamp()
                            )
            round2.save()

            game1 = Games(team_a='team_a', team_b='team_b', score='1-1', match_date=int(datetime.utcnow().timestamp()),
                          match_group="A", round_id=1)
            game2 = Games(team_a='team_c', team_b='team_d', score='2-1', match_date=int(datetime.utcnow().timestamp()),
                          match_group="B", round_id=2)

            game1.create()
            game2.create()

    def test1_new_predictions(self):
        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 1, 'score2': 2},
                                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 0}]}

        res = self.client().post('/api/user-actions/update-predictions',
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

        self.client().post('/api/user-actions/update-predictions',
                           json=data, headers=header_obj)

        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 3, 'score2': 1},
                                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 1}]}

        res = self.client().post('/api/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(201, res.status_code)

    def test3_jwt_expired(self):
        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=0.01)
        time.sleep(1)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 1, 'score2': 2},
                                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 0}]}

        res = self.client().post('/api/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(401, res.status_code)

    def test4_user_not_found_in_database(self):
        jwt = generate_jwt({'email': 'fault_email@yahoo.com'})
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'team_a', 'team2': 'team_b', 'score1': 1, 'score2': 2},
                                {'team1': 'team_c', 'team2': 'team_d', 'score1': 1, 'score2': 0}]}

        res = self.client().post('/api/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(401, res.status_code)

    def test5_update_prediction_but_game_does_not_exist(self):
        with self.app.app_context():
            game_id = uuid.uuid4()
            game1 = Games(id=game_id, team_a='team_z', team_b='team_y', score='1-1', match_date=datetime.utcnow(),
                          match_group='A')
            game1.create()

            prediction = Predictions(game_id=game_id,
                                     user_email=self.user_data['email'],
                                     predicted_score='2-1')
            prediction.create()

        jwt = generate_jwt({'email': self.user_data['email']})
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        data = {'predictions': [{'team1': 'wrong_teama', 'team2': 'wrong_teamb', 'score1': 1, 'score2': 2}]}

        res = self.client().post('/api/user-actions/update-predictions',
                                 json=data, headers=header_obj)

        self.assertEqual(422, res.status_code)

    def test6_get_ranking_no_scores_yet(self):
        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        res = self.client().get('/api/user-actions/get-ranking',
                                headers=header_obj)
        data = res.get_json()['data']
        expected_result = [{'position': 1, 'name': 'Test', 'lastName': 'File', 'points': ''},
                           {'position': 1, 'name': 'Sample', 'lastName': 'File', 'points': ''}]
        self.assertEqual(200, res.status_code)
        for i in range(len(expected_result)):
            diff = DeepDiff(expected_result[i], data[i])
            self.assertEqual(0, len(diff), 'something is wrong')

    def test7_get_ranking_mixture_of_scores(self):
        with self.app.app_context():
            password_hash = bcrypt.generate_password_hash('1234')
            id1 = uuid.uuid4()
            new_user_data = {"id": id1, "email": 'test5@gmail.com',
                             "name": 'Test', "last_name": 'File1',
                             "password": password_hash,
                             "total_points": 5
                             }
            new_user = Users(**new_user_data)
            new_user.create()

            id2 = uuid.uuid4()
            new_user_data1 = {"id": id2,
                              "email": 'test4@gmail.com',
                              "name": 'Sample', "last_name": 'File2',
                              "password": password_hash,
                              "total_points": 1}
            new_user = Users(**new_user_data1)
            new_user.create()

        jwt = generate_jwt({'email': self.user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        res = self.client().get('/api/user-actions/get-ranking',
                                headers=header_obj)
        data = res.get_json()['data']
        expected_result = [{'position': 1, 'name': 'Test', 'lastName': 'File1', 'points': 5},
                           {'position': 2, 'name': 'Sample', 'lastName': 'File2', 'points': 1},
                           {'position': 3, 'name': 'Test', 'lastName': 'File', 'points': ''},
                           {'position': 3, 'name': 'Sample', 'lastName': 'File', 'points': ''}]
        self.assertEqual(200, res.status_code)
        for i in range(len(expected_result)):
            diff = DeepDiff(expected_result[i], data[i])
            self.assertEqual(0, len(diff), 'something is wrong')

    def test8_get_user_predictions(self):
        timestamp = int(datetime.utcnow().timestamp())
        with self.app.app_context():
            password_hash = bcrypt.generate_password_hash('1234')
            id1 = uuid.uuid4()
            id2 = uuid.uuid4()
            id3 = uuid.uuid4()
            new_user_data = {"email": 'test90@gmail.com',
                             "name": 'Test', "last_name": 'File1',
                             "password": password_hash,
                             "total_points": 5
                             }
            new_user = Users(**new_user_data)
            new_user.create()
            game1 = Games(id=id1, team_a='team_a', team_b='team_b', score='1-1',
                          match_date=timestamp, match_group='B', round_id=1)
            game2 = Games(id=id2, team_a='team_a', team_b='team_b', score='1-1',
                          match_date=timestamp, match_group='A', round_id=2)
            game3 = Games(id=id3, team_a='team_a', team_b='team_b', score='1-1',
                          match_date=timestamp, match_group='B', round_id=2)
            game1.create()
            game2.create()
            game3.create()
            new_prediction = Predictions(game_id=id1, user_email=new_user_data["email"],
                                         predicted_score='1-1')
            new_prediction.create()
            new_prediction = Predictions(game_id=id3, user_email=new_user_data["email"],
                                         predicted_score='1-1')
            new_prediction.create()
            round2 = Rounds(id=3, round_name="round3", round_start_datetime='2022-01-01 00:00:00',
                            round_start_timestamp=datetime.utcnow().timestamp(),
                            round_end_datetime='2022-01-02 00:00:00',
                            round_end_timestamp=datetime.utcnow().timestamp()
                            )
            round2.save()

        jwt = generate_jwt({'email': new_user_data['email']}, expiration_time=5)
        header_obj = {
            "Content-Type": 'application/json',
            "Auth-token": jwt
        }
        res = self.client().get('/api/user-actions/get-user-predictions?round_id=1',
                                headers=header_obj)
        data = res.get_json()['data']
        self.assertEqual(200, res.status_code)

        expected_result = [{'games': {'A': [{'ActualScore': '1-1', 'DateTimestamp': timestamp, 'TeamA': 'team_a',
                                             'TeamB': 'team_b', 'UserPredictedScore': ''}],
                                      'B': [{'ActualScore': '1-1', 'DateTimestamp': timestamp, 'TeamA': 'team_a',
                                             'TeamB': 'team_b', 'UserPredictedScore': '1-1'}]},
                            }]

        for i in range(len(data)):

            diff = DeepDiff(expected_result[i], data[i])
            self.assertEqual(0, len(diff), 'something is wrong')

    def tearDown(self) -> None:
        with self.app.app_context():
            db.drop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()
