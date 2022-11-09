import logging
import re
import sqlalchemy.exc
from flask import Blueprint
from flask_pydantic import validate
from pydantic import BaseModel, Field, validator
from werkzeug.exceptions import Unauthorized

from flaskr.db.users import Users
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import generate_jwt
from flaskr.utils.extensions import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')

logger = logging.getLogger(__name__)


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


class LoginBody(BaseModel):
    email: str
    password: str = Field(min_length=3, max_length=20)


@bp.route('/register', methods=['POST'])
@validate(body=RegisterBody)
def register(body: RegisterBody):
    try:
        password_hash = bcrypt.generate_password_hash(body.password)
        new_user = Users(email=body.email,
                         name=body.name, last_name=body.last_name,
                         password=password_hash)
        new_user.insert()
        logger.info('User successfully created!')
        response = CustomResponse(message='Usuario fue creado exitosamente', status_code=201)
        return response.custom_jsonify()
    except sqlalchemy.exc.IntegrityError as e:
        error = Exception('Usuario ya existe! Usa otro correo electronico')
        logger.exception(e)
        custom_abort(400, error)


@bp.route('/login', methods=['POST'])
@validate(body=LoginBody)
def login(body: LoginBody):

    try:
        find_user = Users.query.filter_by(email=body.email).first()
        if find_user is None:
            raise Exception('Usuario no esta registrado!')
        check_if_passwords_match = bcrypt.check_password_hash(find_user.password, body.password)
        if check_if_passwords_match:
            jwt = generate_jwt(str(find_user.id))
            return CustomResponse(message='Iniciando sesión!', data={'token': jwt}).custom_jsonify()

        raise Unauthorized(description='La contraseña ingresada no es correct!')

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(400, e)




