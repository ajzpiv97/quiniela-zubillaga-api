from flask import Blueprint
from flaskr.utils.custom_response import CustomResponse

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def status():
    response = CustomResponse(message='up')
    return response.custom_jsonify()


