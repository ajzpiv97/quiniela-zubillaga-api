import os
from datetime import datetime, timedelta
import jwt


SECRET_KEY = os.environ.get('SECRET_KEY', 'api')


def generate_jwt(user_id: str, expiration_time: int = 60) -> str:
    token = jwt.encode(
        {'id': user_id, 'expiration_date': str(datetime.utcnow() + timedelta(minutes=expiration_time))},
        SECRET_KEY, "HS256")

    return token


def decode_jwt(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
