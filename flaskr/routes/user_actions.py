import logging
from flask import Blueprint
from flask_pydantic import validate
from werkzeug.exceptions import UnprocessableEntity, BadRequest, NotFound, Unauthorized
from flaskr.db.games import Games
from flaskr.db.predictions import Predictions
from flaskr.db.users import Users
from flaskr.models.models import PredictionBody
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import authenticate_user

bp = Blueprint('user_actions', __name__, url_prefix='/api/user-actions')

logger = logging.getLogger(__name__)


@bp.route('/update-predictions', methods=['POST'])
@validate(body=PredictionBody)
def update_predictions(body: PredictionBody):
    try:
        decoded_token, find_user = authenticate_user()

        # find if user has made any predictions yet
        find_pred = Predictions.query.filter_by(user_email=decoded_token['email']).first()

        # set new values
        # loop , get game id with teams, get user id and update prediction
        for game in body.predictions:
            # get game
            find_game = Games.query.filter_by(team_a=game.team1, team_b=game.team2).first()
            if find_game is None:
                find_game = Games.query.filter_by(team_a=game.team2, team_b=game.team1).first()
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
                temp_pred_obj = Predictions.query.filter_by(game_id=find_game.id, user_email=find_user.email).first()
                temp_pred_obj.update(predicted_score=f'{game.score1}-{game.score2}')
                logger.info("Update prediction made by user " + str(find_user.email))

    except UnprocessableEntity as e:
        logger.exception(e)
        custom_abort(422, e)

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(400, e)

    return CustomResponse(message='Update successful!', status_code=201).custom_jsonify()


@bp.route('/get-ranking', methods=['GET'])
def get_ranking():
    try:
        authenticate_user(return_values=False)
        rankings = Users.query.order_by(Users.total_points.desc()).all()
        current_position = 1
        current_points = rankings[0].total_points
        ranking_order = []
        for rank in rankings:
            if rank.total_points != current_points:
                current_position += 1

            ranking_order.append(
                {'position': current_position, 'name': rank.name, 'lastName': rank.last_name,
                 'points': rank.total_points if rank.total_points > -1 else ''})

            current_points = min(rank.total_points, current_points)

        return CustomResponse(message='Generate ranking result', data=ranking_order).custom_jsonify()

    except BadRequest as e:
        logger.exception(e)
        custom_abort(400, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(500, e)


@bp.route('/get-user-predictions', methods=['GET'])
def get_user_predictions():
    try:
        decoded_token, find_user = authenticate_user()
        games = Games.query.all()

        if len(games) == 0:
            raise NotFound('No games found!')

        ret_dict = {
        }

        for game in games:
            prediction = Predictions.query.filter_by(user_email=decoded_token['email'], game_id=game.id).first()
            if game.group in ret_dict:
                ret_dict[game.group].append({'TeamA': game.team_a, 'TeamB': game.team_b,
                                             'UserPredictedScore': '' if prediction is None
                                             else prediction.predicted_score,
                                             'ActualScore': game.score})
            else:
                ret_dict[game.group] = [{'TeamA': game.team_a, 'TeamB': game.team_b,
                                         'UserPredictedScore': '' if prediction is None
                                         else prediction.predicted_score,
                                         'ActualScore': game.score}]

        return CustomResponse(message='Predictions per game per user!', data=ret_dict).custom_jsonify()

    except NotFound as e:
        logger.exception(e)
        custom_abort(404, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(500, e)
