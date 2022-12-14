import logging
from flask import Blueprint, request
from flask_pydantic import validate
from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity, BadRequest, NotFound, Unauthorized
from flaskr.db.games import Games
from flaskr.db.predictions import Predictions
from flaskr.db.rounds import Rounds
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

        # loop , get game id with teams, get user id and update prediction
        time = datetime.utcnow()
        for game in body.predictions:
            # get game
            find_game = Games.query.filter_by(team_a=game.team1, team_b=game.team2).first()
            if find_game is None:
                find_game = Games.query.filter_by(team_a=game.team2, team_b=game.team1).first()
                if find_game is None:
                    raise UnprocessableEntity("no game found between " + game.team1 + " vs " + game.team2)

            temp_pred_obj = Predictions.query.filter_by(game_id=find_game.id, user_email=find_user.email).first()
            if temp_pred_obj is None:
                temp_pred_obj = Predictions(game_id=find_game.id, user_email=find_user.email,
                                            predicted_score=f'{game.score1}-{game.score2}',
                                            prediction_insert_date=time)
                temp_pred_obj.save()
                logger.info(f'Created prediction! User: {find_user.email}')
            else:
                temp_pred_obj.update(predicted_score=f'{game.score1}-{game.score2}',
                                     prediction_modified_date=time)
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

            if current_position != rank.current_ranking:
                rank.update(current_ranking=current_position, past_ranking=rank.current_ranking)

            ranking_order.append(
                {'position': current_position, 'name': rank.name, 'lastName': rank.last_name,
                 'points': rank.total_points if rank.total_points > -1 else '',
                 'positionMove': rank.past_ranking - rank.current_ranking})

            current_points = min(rank.total_points, current_points)

        return CustomResponse(message='Generate ranking result', data=ranking_order).custom_jsonify()

    except BadRequest as e:
        logger.exception(e)
        custom_abort(400, e)

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(500, e)


@bp.route('/get-rounds', methods=['GET'])
def get_rounds():
    try:
        authenticate_user()
        rounds = Rounds.query.order_by(Rounds.id).all()

        if len(rounds) == 0:
            raise BadRequest('No round were found!')

        rounds_list = []

        for game_round in rounds:
            round_info = {'id': game_round.id, 'name': game_round.round_name,
                          'startTimestamp': game_round.round_start_timestamp,
                          'endTimestamp': game_round.round_end_timestamp,
                          'startPredictionTimestamp': game_round.prediction_start_timestamp,
                          'endPredictionTimestamp': game_round.prediction_end_timestamp
                          }
            rounds_list.append(round_info)

        return CustomResponse(message='Predictions per game per user!', data=rounds_list).custom_jsonify()

    except NotFound as e:
        logger.exception(e)
        custom_abort(404, e)

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

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
        round_id = request.args.get('roundId')

        if round_id is None:
            raise BadRequest('No round id was passed!')

        game_round = Rounds.query.filter_by(id=round_id).first()

        if game_round is None:
            raise NotFound('No round found!')

        ret_dict = {
        }

        rounds_list = []

        round_info = {}
        for game in game_round.games:
            prediction = Predictions.query.filter_by(user_email=decoded_token['email'], game_id=game.id).first()
            prediction_obj = {'TeamA': game.team_a, 'TeamB': game.team_b,
                              'UserPredictedScore': '' if prediction is None
                              else prediction.predicted_score,
                              'ActualScore': game.score,
                              'DateTimestamp': game.match_date}

            if game.match_group in ret_dict:
                ret_dict[game.match_group].append(prediction_obj)
            else:
                ret_dict[game.match_group] = [prediction_obj]

        round_info['games'] = ret_dict
        rounds_list.append(round_info)
        return CustomResponse(message='Predictions per game per user!', data=rounds_list).custom_jsonify()

    except NotFound as e:
        logger.exception(e)
        custom_abort(404, e)

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except BadRequest as e:
        logger.exception(e)
        custom_abort(400, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(500, e)
