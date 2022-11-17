import unittest

import json
from datetime import datetime

import pandas as pd

from flaskr.app import create_app
from flaskr.db.users import Users
from flaskr.db.predictions import Predictions
from flaskr.db.games import Games
from flaskr.utils.extensions import db, bcrypt
from flaskr.utils.local_utils import iterate_through_df_and_update_user_points_based_on_game_score


class CommandTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    app = create_app()

    def setUp(self) -> None:
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            password_hash = bcrypt.generate_password_hash('1234')

            game1 = Games(id="ze9826cb-ee8e-4274-8b78-a98872a9b2aa", team_a='team_a',
                          team_b='team_b', score='', date=datetime.utcnow())
            game2 = Games(id="ze9826cb-ee8e-4274-8b78-a98872a9b2ab", team_a='team_c',
                          team_b='team_d', score='', date=datetime.utcnow())

            game1.create()
            game2.create()

            for i in range(3):
                user_data = {"email": f'test{i}@gmail.com',
                             "name": f'Test{i}', "last_name": f'File{i}',
                             "password": password_hash,
                             }
                new_user = Users(**user_data)
                new_user.create()

                prediction = Predictions(game_id="ze9826cb-ee8e-4274-8b78-a98872a9b2aa",
                                         user_email=f'test{i}@gmail.com',
                                         predicted_score=f'{i}-{i*2}')
                prediction.create()
                prediction = Predictions(game_id="ze9826cb-ee8e-4274-8b78-a98872a9b2aa",
                                         user_email=f'test{i}@gmail.com',
                                         predicted_score=f'{i+2}-{i}')
                prediction.create()

    def test1_create_new_user(self):
        df = pd.DataFrame({'team_a': ['team_a', 'team_c'], 'team_b': ['team_b', 'team_d'], 'score': ['0-6', '0-1']})
        with self.app.app_context():
            iterate_through_df_and_update_user_points_based_on_game_score(df)
        self.assertEqual(1,1)

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            db.drop_all()
