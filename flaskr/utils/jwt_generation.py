from datetime import datetime, timedelta
import jwt
from flask import Flask

app = Flask(__name__)


def generate_jwt(user_id: str, expiration_time: int = 45) -> str:
    token = jwt.encode(
        {'id': user_id, 'expiration_date': str(datetime.utcnow() + timedelta(minutes=expiration_time))},
        app.config['SECRET_KEY'], "HS256")

    return token
