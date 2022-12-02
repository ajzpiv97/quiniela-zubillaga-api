import logging
import pandas as pd
import pytz

import re
from typing import NoReturn
from datetime import datetime
from flaskr.db.games import Games
from flaskr.db.users import Users

logger = logging.getLogger(__name__)


def get_score(actual_score: str, predicted_score: str) -> int:
    if predicted_score == '-':
        return 0

    score_a = [int(score) for score in actual_score.strip().split("-")]
    score_p = [int(score) for score in predicted_score.strip().split("-")]
    score = 0
    # rule for perfect match
    if score_a[0] == score_p[0] and score_a[1] == score_p[1]:
        return 5
    # rule for same winner
    if (score_p[0] > score_p[1] and score_a[0] > score_a[1]) or (score_p[1] > score_p[0] and score_a[1] > score_a[0]):
        score += 3
    elif score_p[0] == score_p[1] and score_a[0] == score_a[1]:
        score += 3

    # score has the correct number of goals
    if score_p[0] + score_p[1] == score_a[0] + score_a[1]:
        score += 2

    return score


def read_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        df.columns = [re.sub(r'\W+', '_', col).lower() for col in df.columns]
        return df
    except Exception as e:
        logger.exception(e)
        raise


def verify_quiniela_columns(df: pd.DataFrame) -> NoReturn:
    if 'team_a' not in df or 'team_b' not in df or 'score' not in df:
        raise ValueError(f'Missing columns: {df.columns}')


def update_user_points_based_on_predictions(games_update_file: str):
    df = read_csv(games_update_file)
    verify_quiniela_columns(df)
    iterate_through_df_and_update_user_points_based_on_game_score(df)


def iterate_through_df_and_update_user_points_based_on_game_score(df: pd.DataFrame):
    for index, row in df.iterrows():
        # get game
        team_a: str = row['team_a'].strip().upper()
        team_b: str = row['team_b'].strip().upper()
        score = row['score']
        game = Games.query.filter_by(team_a=team_a, team_b=team_b).first()
        if game is None:
            game = Games.query.filter_by(team_a=team_b, team_b=team_a).first()
            if game is None:
                raise Exception(f'Game -> {team_a} vs {team_b} not found')
        if game.score == score:
            logger.warning('Game was already updated!')
        else:
            game.update(score=score)
            predictions = game.predictions
            for prediction in predictions:
                points = get_score(score, prediction.predicted_score)
                prediction.update(actual_score=score, points=points)
                user = Users.query.filter_by(email=prediction.user_email).first()
                current_points = 0 if user.total_points == -1 else user.total_points
                points += current_points
                user.update(total_points=points)


def get_datetime_object_from_pattern(date, time) -> datetime:
    pattern = '%m/%d/%y %H:%M:%S'
    tz = pytz.timezone('UTC')
    datetime_obj = datetime.strptime(f"{date} {time}", pattern).astimezone(tz)
    return datetime_obj
