import uuid

import pandas as pd
import unittest
from datetime import datetime

from flaskr.app import create_app
from flaskr.db.users import Users
from flaskr.db.predictions import Predictions
from flaskr.db.games import Games
from flaskr.utils.extensions import db, bcrypt
from flaskr.utils.local_utils import iterate_through_df_and_update_user_points_based_on_game_score


class CommandTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    app = create_app()
    game_id1 = uuid.uuid4()
    game_id2 = uuid.uuid4()

    def setUp(self) -> None:
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            password_hash = bcrypt.generate_password_hash('1234')

            game1 = Games(id=self.game_id1, team_a='TEAM_A',
                          team_b='TEAM_B', score='', match_date=datetime.utcnow(), match_group='A')
            game2 = Games(id=self.game_id2, team_a='TEAM_C',
                          team_b='TEAM_D', score='', match_date=datetime.utcnow(), match_group='B')

            game1.create()
            game2.create()

            for i in range(3):
                user_data = {"email": f'test{i}@gmail.com',
                             "name": f'Test{i}', "last_name": f'File{i}',
                             "password": password_hash,
                             }
                new_user = Users(**user_data)
                new_user.create()

                prediction = Predictions(game_id=self.game_id1,
                                         user_email=f'test{i}@gmail.com',
                                         predicted_score=f'{i}-{i*2}')
                prediction.create()
                prediction = Predictions(game_id=self.game_id2,
                                         user_email=f'test{i}@gmail.com',
                                         predicted_score=f'{i+2}-{i}')
                prediction.create()

    def test1_update_points_for_users(self):
        df = pd.DataFrame({'team_a': ['TEAM_A', 'TEAM_C'], 'team_b': ['TEAM_B', 'TEAM_D'], 'score': ['0-6', '2-1']})
        with self.app.app_context():
            iterate_through_df_and_update_user_points_based_on_game_score(df)
            self.assertEqual(3, Users.query.filter_by(email='test0@gmail.com').first().total_points,
                             'something is wrong')
            self.assertEqual(6, Users.query.filter_by(email='test1@gmail.com').first().total_points,
                             'something is wrong')
            self.assertEqual(8, Users.query.filter_by(email='test2@gmail.com').first().total_points,
                             'something is wrong')

    def test2_update_points_already_updated(self):
        df = pd.DataFrame({'team_a': ['TEAM_A', 'TEAM_C'], 'team_b': ['TEAM_B', 'TEAM_D'], 'score': ['0-6', '2-1']})
        with self.app.app_context():
            game = Games.query.filter_by(id=self.game_id2).first()
            game.update(score='2-1')
            iterate_through_df_and_update_user_points_based_on_game_score(df)
            self.assertEqual(0, Users.query.filter_by(email='test0@gmail.com').first().total_points,
                             'something is wrong')
            self.assertEqual(3, Users.query.filter_by(email='test1@gmail.com').first().total_points,
                             'something is wrong')
            self.assertEqual(5, Users.query.filter_by(email='test2@gmail.com').first().total_points,
                             'something is wrong')

    def test3_fail_to_update_score_game_does_not_exist(self):
        df = pd.DataFrame({'team_a': ['team_f', 'team_c'], 'team_b': ['team_b', 'team_d'], 'score': ['0-6', '2-1']})
        with self.app.app_context():
            with self.assertRaises(Exception) as e:
                iterate_through_df_and_update_user_points_based_on_game_score(df)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()

    def tearDown(self) -> None:
        with self.app.app_context():
            db.drop_all()
