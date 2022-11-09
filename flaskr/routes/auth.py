import re
import sqlalchemy.exc
from flask import Blueprint, Flask, Response, jsonify
from flask_pydantic import validate
from pydantic import BaseModel, Field, validator

from flaskr.db.users import Users
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort

bp = Blueprint('auth', __name__, url_prefix='/auth')

app = Flask(__name__)


class RegisterBody(BaseModel):
    email: str
    name: str
    last_name: str = Field(alias='lastName')
    password: str = Field(min_length=3, max_length=20)

    # custom validation on email field
    @validator('email')
    def email_valid(cls, value: str) -> str:
        """
        Method to validate email is correct
        :param value: current email value
        :return: email value
        """
        email = value.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('Email provided is not valid!')
        return email


@bp.route('/register', methods=['POST'])
@validate(body=RegisterBody)
def register(body: RegisterBody):
    try:
        new_user = Users(email=body.email,
                         name=body.name, last_name=body.last_name,
                         password=body.password)
        new_user.insert()
        app.logger.info('User successfully created!')
        response = CustomResponse(message='message', status_code=201)
        return response.custom_jsonify()
    except sqlalchemy.exc.IntegrityError as e:
        error = Exception('Usuario ya existe! Usa otro correo electronico')
        app.logger.exception(e)
        custom_abort(400, error)

