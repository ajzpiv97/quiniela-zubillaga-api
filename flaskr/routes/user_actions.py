import logging
from flask import Blueprint, request
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized
from datetime import datetime
from flaskr.db.games import Games
from flaskr.db.predictions import Predictions
from flaskr.db.users import Users
from flaskr.models.models import PredictionBody
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import decode_jwt

bp = Blueprint('user_actions', __name__, url_prefix='/user_actions')

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
        token = request.headers['Auth-token']

        decoded_token = decode_jwt(token)

        if decoded_token['expiration_date'] < datetime.utcnow():
            raise Unauthorized("Token not valid")

        find_user = Users.query.filter_by(email=decoded_token['email']).first()
        if find_user is None:
            raise Unauthorized('Usuario no esta registrado!')

        # find if user has made any predictions yet
        find_pred = Predictions.query.filter_by(email=decoded_token['email']).first()

        # set new values
        # loop , get game id with teams, get user id and update prediction
        for game in body:

            # get game
            find_game = Games.query.filter_by(team_a=game['team1'], team_b=game['team2'])
            if find_game is None:
                find_game = Games.query.filter_by(team_a=game['team2'], team_b=game['team1'])
                if find_game is None:
                    raise Exception("no game found between " + game['team1'] + " vs " + game['team2'])
            if find_pred is None:

                # create new
                new_pred = Predictions(game=find_game.id, user=find_user.email,
                                       predicted_score=str(game['score1'] + "-" + game['score2']))
                new_pred.create()
                logger.info("New prediction made by user " + str(find_user.email))
            else:
                # update
                # get object
                temp_pred_obj = Predictions.query.filter_by(game=find_game.id, user=find_user.email)
                temp_pred_obj.update(predicted_score=str(game['score1'] + "-" + game['score2']))
                logger.info("Update prediction made by user " + str(find_user.email))

        logger.info("Something went wrong with the user")

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except Exception as e:
        logger.error(str(e))
        custom_abort(500, e)

    return CustomResponse(message='Update successful!').custom_jsonify()
