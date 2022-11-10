import logging
import sqlalchemy.exc
from flask import Blueprint
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized

from flaskr.db.games import Games
from flaskr.models.models import RegisterBody, LoginBody
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import generate_jwt
from flaskr.utils.extensions import bcrypt

bp = Blueprint('user_actions', __name__, url_prefix='/user_actions')

logger = logging.getLogger(__name__)



##TODO
'''
- post: token and payload(list of dictonaries of game results)
- update or create db entries fro each games predictions
- token: 1. decrypt 
         2. use that for creating the data
- test 
'''

@bp.route('/update-predictions', methods=['POST'])
##@validate(body=LoginBody)
def login():
    return CustomResponse(message='Testing api').custom_jsonify()

