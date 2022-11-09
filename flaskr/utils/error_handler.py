from flask import json, Flask, abort
from werkzeug.exceptions import HTTPException


def error_handler(app: Flask):  # pragma: no cover
    @app.errorhandler(HTTPException)
    def handle_exception(e) -> str:
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response


def custom_abort(code: int, error: Exception):  # pragma: no cover
    abort(code, str(error))
