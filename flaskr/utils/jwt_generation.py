import logging
from datetime import datetime, timedelta
from typing import Dict

import jwt
from flask import request
from werkzeug.exceptions import Unauthorized

from flaskr.db.users import Users
from flaskr.utils.env_variables import SECRET_KEY
from flaskr.utils.error_handler import custom_abort

logger = logging.getLogger(__name__)


def generate_jwt(payload: Dict, expiration_time: float = 60.0) -> str:
    token = jwt.encode(
        {**payload, 'expiration_date': str(datetime.utcnow() + timedelta(minutes=expiration_time))},
        SECRET_KEY, "HS256")

    return token


def decode_jwt(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload


def authenticate_user(return_values: bool = True):
    try:
        token = request.headers['Auth-token']
        decoded_token = decode_jwt(token)
        if decoded_token['expiration_date'] < str(datetime.utcnow()):
            raise Unauthorized("Token not valid")
        find_user = Users.query.filter_by(email=decoded_token['email']).first()
        if find_user is None:
            raise Unauthorized('Usuario no esta registrado!')
        if return_values:
            return decoded_token, find_user
    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)


