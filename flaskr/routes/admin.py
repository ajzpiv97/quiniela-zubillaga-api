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

bp = Blueprint('admin', __name__, url_prefix='/admin')

logger = logging.getLogger(__name__)

