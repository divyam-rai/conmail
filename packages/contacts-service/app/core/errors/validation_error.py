from werkzeug.exceptions import HTTPException
from app.core.helpers.utils import response

class ValidationError(HTTPException):
    code: int = 400

    def __init__(self, description: str):
        resp = response(self.code, { "error": description })
        super().__init__(description=description, response=resp)
