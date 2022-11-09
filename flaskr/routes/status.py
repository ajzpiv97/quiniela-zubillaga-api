from flask import Blueprint, Flask, Response, jsonify

from flaskr.utils.custom_response import CustomResponse

bp = Blueprint('status', __name__, url_prefix='/')

app = Flask(__name__)


@bp.route('/', methods=['GET'])
def status():
    response = CustomResponse(message='up')
    return response.custom_jsonify()


