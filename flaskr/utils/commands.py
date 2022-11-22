import click
import logging
import pandas as pd
from flask.cli import with_appcontext
from flaskr.db.games import Games
from flaskr.utils.extensions import db
from flaskr.utils.local_utils import update_user_points_based_on_predictions
from flaskr.utils.local_utils import get_timestamp
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
            new_game = Games(team_a=data.iloc[i]['equipo1'].strip().upper(),
                             team_b=data.iloc[i]['equipo2'].strip().upper(),
                             date=data.iloc[i]['fecha'],
                             group=data.iloc[i]['grupo'])
            new_game.save()
            logger.info('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
            print('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
        except Exception as e:
            print(e)
            print("error logging games")


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
            utc_timestamp = get_timestamp(date, time)
            temp_game_obj.update(match_date=utc_timestamp)
            temp_game_obj.save()
            logger.info('Game successfully updated!' + data.iloc[i]['date'])
            print('Game successfully updated!' + data.iloc[i]['date'])
        except Exception as e:
            print(e)
            print("error updating game date")