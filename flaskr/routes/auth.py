import logging
import sqlalchemy.exc
from flask import Blueprint
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized

from flaskr.db.users import Users
from flaskr.db.games import Games
from flaskr.models.models import RegisterBody, LoginBody
from flaskr.utils.custom_response import CustomResponse
from flaskr.utils.error_handler import custom_abort
from flaskr.utils.jwt_generation import generate_jwt
from flaskr.utils.extensions import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')

logger = logging.getLogger(__name__)


@bp.route('/register', methods=['POST'])
@validate(body=RegisterBody)
def register(body: RegisterBody):
    try:
        password_hash = bcrypt.generate_password_hash(body.password)
        new_user = Users(email=body.email,
                         name=body.name, last_name=body.last_name,
                         password=password_hash)
        new_user.save()
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
            jwt = generate_jwt(str(find_user.email))
            return CustomResponse(message='Iniciando sesión!', data={'token': jwt}).custom_jsonify()

        raise Unauthorized(description='La contraseña ingresada no es correct!')

    except Unauthorized as e:
        logger.exception(e)
        custom_abort(401, e)

    except Exception as e:
        logger.exception(e)
        custom_abort(400, e)




