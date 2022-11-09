import os
from datetime import datetime, timedelta
import jwt


def generate_jwt(user_id: str, expiration_time: int = 45) -> str:
    token = jwt.encode(
        {'id': user_id, 'expiration_date': str(datetime.utcnow() + timedelta(minutes=expiration_time))},
        os.environ.get('SECRET_KEY'), "HS256")

    return token
