import click
import logging
import pandas as pd
from flask.cli import with_appcontext
from flaskr.db.games import Games
from flaskr.db.rounds import Rounds
from flaskr.utils.extensions import db
from flaskr.utils.local_utils import update_user_points_based_on_predictions
from flaskr.utils.local_utils import get_datetime_object_from_pattern

logger = logging.getLogger(__name__)


@click.command(name='db')
@with_appcontext
def migrate(app):
    migrate.init_app(app, db)


@click.command(name="update_games")
@click.option('--games-update-file')
@with_appcontext
def populate(games_update_file):
    update_user_points_based_on_predictions(games_update_file)


@click.command(name="init_games")
@click.option('--file')
@with_appcontext
def init_games(file):
    data = pd.read_csv(file)
    print(data.shape[0])
    for i in range(data.shape[0]):
        try:
            date = data.iloc[i]["date"]
            time = data.iloc[i]["time"]
            utc_timestamp = get_datetime_object_from_pattern(date, time).timestamp()
            new_game = Games(team_a=data.iloc[i]['equipo1'].strip().upper(),
                             team_b=data.iloc[i]['equipo2'].strip().upper(),
                             match_date=utc_timestamp,
                             match_group=data.iloc[i]['grupo'],
                             round_id=int(data.iloc[i]['ronda']))
            new_game.save()
            logger.info('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
            print('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
        except Exception as e:
            print(e)
            print("error logging games")


@click.command(name="init_rounds")
@click.option('--file')
@with_appcontext
def init_rounds(file):
    data = pd.read_csv(file)
    print(data.shape[0])
    for i in range(data.shape[0]):
        try:
            start_date = data.iloc[i]["start_date"]
            start_time = data.iloc[i]["start_time"]
            end_date = data.iloc[i]["end_date"]
            end_time = data.iloc[i]["end_time"]
            start_utc_object = get_datetime_object_from_pattern(start_date, start_time)
            end_utc_object = get_datetime_object_from_pattern(end_date, end_time)

            start_date_pred = data.iloc[i]["start_date_pred"]
            start_time_pred = data.iloc[i]["start_time_pred"]
            end_date_pred = data.iloc[i]["end_date_pred"]
            end_time_pred = data.iloc[i]["end_time_pred"]

            start_pred_utc_object = get_datetime_object_from_pattern(start_date_pred, start_time_pred) \
                if not pd.isna(start_date_pred) else None
            end_pred_utc_object = get_datetime_object_from_pattern(end_date_pred, end_time_pred) \
                if not pd.isna(end_date_pred) else None

            new_round = Rounds(round_name=data.iloc[i]['round'].strip().upper(),
                               round_start_datetime=start_utc_object.strftime("%Y-%m-%d %H:%M:%S"),
                               round_start_timestamp=start_utc_object.timestamp(),
                               round_end_datetime=end_utc_object.strftime("%Y-%m-%d %H:%M:%S"),
                               round_end_timestamp=end_utc_object.timestamp(),
                               prediction_start_timestamp=start_pred_utc_object.timestamp() if start_pred_utc_object
                                                                                            is not None else None,
                               prediction_end_timestamp=end_pred_utc_object.timestamp() if end_pred_utc_object
                                                                                            is not None else None,
                               )
            new_round.save()
            logger.info('Round successfully created!' + data.iloc[i]['round'])
            print('Round successfully created!' + data.iloc[i]['round'])
        except Exception as e:
            print(e)
            print("error logging round")


@click.command(name="update_game_time")
@click.option('--file')
@with_appcontext
def update_game_time(file):
    data = pd.read_csv(file)
    print(data.shape[0])
    for i in range(data.shape[0]):
        try:
            temp_game_obj = Games.query.filter_by(team_a=data.iloc[i]['team_a'], team_b=data.iloc[i]['team_b'],
                                                  match_group=data.iloc[i]['grupo']).first()
            date = data.iloc[i]["date"]
            time = data.iloc[i]["time"]
            utc_timestamp = get_datetime_object_from_pattern(date, time).timestamp()
            temp_game_obj.update(match_date=utc_timestamp)
            temp_game_obj.save()
            logger.info('Game successfully updated!' + data.iloc[i]['date'])
            print('Game successfully updated!' + data.iloc[i]['date'])
        except Exception as e:
            print(e)
            print("error updating game date")
