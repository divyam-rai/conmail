from werkzeug.exceptions import HTTPException
from app.core.helpers.utils import response

class NotFound(HTTPException):
    code: int = 404

    def __init__(self, resource: str = "resource"):
        resp = response(self.code, { "error": f'{resource} not found' })
        super().__init__(response=resp)
