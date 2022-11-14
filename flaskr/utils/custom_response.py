from typing import Optional, Dict, Any
from flask import jsonify


class CustomResponse:
    def __init__(self, message: str, data: Optional[Any] = None, status_code: int = 200):
        self.message = message
        self.data = data
        self.status_code = status_code

    def custom_jsonify(self):
        return jsonify(message=self.message, data=self.data), self.status_code
