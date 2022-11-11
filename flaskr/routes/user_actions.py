import logging
from flask import Blueprint
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized, UnprocessableEntity
from flaskr.db.games import Games
from flaskr.db.predictions import Predictions
from flaskr.models.models import PredictionBody
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import authenticate_user

bp = Blueprint('user_actions', __name__, url_prefix='/user-actions')

logger = logging.getLogger(__name__)

# TODO
'''
- post: token and payload(list of dictonaries of game results)
- update or create db entries fro each games predictions
- token: 1. decrypt 
         2. use that for creating the data
- test 
'''


@bp.route('/update-predictions', methods=['POST'])
@validate(body=PredictionBody)
def update_predictions(body: PredictionBody):
    try:
        print(body.predictions)
        decoded_token, find_user = authenticate_user()

        # find if user has made any predictions yet
        find_pred = Predictions.query.filter_by(user_email=decoded_token['email']).first()

        # set new values
        # loop , get game id with teams, get user id and update prediction
        for game in body.predictions:
            # get game
            find_game = Games.query.filter_by(team_a=game.team1, team_b=game.team2).one()
            if find_game is None:
                find_game = Games.query.filter_by(team_a=game.team2, team_b=game.team1).one()
                if find_game is None:
                    raise UnprocessableEntity("no game found between " + game.team1 + " vs " + game.team2)
            if find_pred is None:

                # create new
                new_pred = Predictions(game_id=find_game.id, user_email=find_user.email,
                                       predicted_score=f'{game.score1}-{game.score2}')
                new_pred.create()
                logger.info("New prediction made by user " + str(find_user.email))
            else:
                # update
                # get object
                temp_pred_obj = Predictions.query.filter_by(game_id=find_game.id, user_email=find_user.email).one()
                temp_pred_obj.update(predicted_score=f'{game.score1}-{game.score2}')
                logger.info("Update prediction made by user " + str(find_user.email))

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except UnprocessableEntity as e:
        logger.exception(e)
        custom_abort(422, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(400, e)

    return CustomResponse(message='Update successful!', status_code=201).custom_jsonify()

