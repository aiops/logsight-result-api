from http import HTTPStatus

from pydantic import BaseModel


class Response(BaseModel):
    app_id: str
    message: str


class ErrorResponse(Response):
    def __init__(self, id, message):
        super(ErrorResponse, self).__init__(app_id=id, message=message)


class SuccessResponse(Response):
    def __init__(self, id, message):
        super(SuccessResponse, self).__init__(app_id=id, message=message)
