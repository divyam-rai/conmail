from werkzeug.exceptions import HTTPException
from app.core.helpers.utils import response

class InternalError(HTTPException):
    code: int = 500

    def __init__(self):
        resp = response(self.code, { "error": 'internal server error' })
        super().__init__(response=resp)
