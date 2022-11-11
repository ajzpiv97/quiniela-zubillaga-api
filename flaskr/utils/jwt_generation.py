import os
from datetime import datetime, timedelta
from typing import Dict

import jwt
from flask import request
from werkzeug.exceptions import Unauthorized

from flaskr.db.users import Users

SECRET_KEY = os.environ.get('SECRET_KEY', 'api')


def generate_jwt(payload: Dict, expiration_time: int = 60) -> str:
    token = jwt.encode(
        {**payload, 'expiration_date': str(datetime.utcnow() + timedelta(minutes=expiration_time))},
        SECRET_KEY, "HS256")

    return token


def decode_jwt(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload


def authenticate_user():
    token = request.headers['Auth-token']
    decoded_token = decode_jwt(token)
    if decoded_token['expiration_date'] < str(datetime.utcnow()):
        raise Unauthorized("Token not valid")
    find_user = Users.query.filter_by(email=decoded_token['email']).first()
    if find_user is None:
        raise Unauthorized('Usuario no esta registrado!')
    return decoded_token, find_user
