from flask import Blueprint, Flask
from flaskr.utils.custom_response import Response

bp = Blueprint('status', __name__, url_prefix='/')

app = Flask(__name__)


@bp.route('/', methods=['GET'])
def status():
    response = Response(code=200, message='up')
    return response.to_json()


