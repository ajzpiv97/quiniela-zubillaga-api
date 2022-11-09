from typing import Optional, Dict
from flask import jsonify


class CustomResponse:
    def __init__(self, message: str, data: Optional[Dict] = None, status_code: int = 200):
        if data is None:
            data = {}
        self.message = message
        self.data = data
        self.status_code = status_code

    def custom_jsonify(self):
        return jsonify(message=self.message, data=self.data, status_code=self.status_code)
