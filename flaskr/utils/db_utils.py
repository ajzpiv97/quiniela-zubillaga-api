import pandas
import logging
from flaskr.db.games import Games
from flaskr.app import create_app

logger = logging.getLogger(__name__)

app = create_app()


def load_games(file):
    data = pandas.read_csv(file)
    print(data.shape[0])

    for i in range(data.shape[0]):
        try:
            new_game = Games(team_a=data.iloc[i]['equipo1'],
                             team_b=data.iloc[i]['equipo2'],
                             date=data.iloc[i]['fecha'],
                             group=data.iloc[i]['grupo'])
            new_game.save()
            logger.info('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
            print('Game successfully created!' + data.iloc[i]['equipo1'] + " VS " + data.iloc[i]['equipo2'])
        except Exception as e:
            print(e)
            print("error logging games")


with app.app_context():
    load_games("data/partidos.csv")
