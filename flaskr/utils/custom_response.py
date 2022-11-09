import json
from typing import Optional, Dict

from flask import Response, jsonify


class CustomResponseHandler(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(CustomResponseHandler, cls).force_type(rv, environ)


class Response:
    def __init__(self, code: int, message: str, data: Optional[Dict] = None):
        if data is None:
            data = {}
        self.code = code
        self.message = message
        self.data = json.dumps(data)

    def to_json(self) -> Dict:
        return self.__dict__
