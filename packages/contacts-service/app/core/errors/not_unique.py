from werkzeug.exceptions import HTTPException
from app.core.helpers.utils import response

class NotUnique(HTTPException):
    code: int = 409

    def __init__(self):
        resp = response(self.code, { "error": "record not unique" })
        super().__init__(response=resp)
