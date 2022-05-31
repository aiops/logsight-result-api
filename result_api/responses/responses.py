from http import HTTPStatus

from pydantic import BaseModel


class Response(BaseModel):
    message: str


class ErrorResponse(Response):
    def __init__(self, message):
        super(ErrorResponse, self).__init__(message=message)


class SuccessResponse(Response):
    def __init__(self, message):
        super(SuccessResponse, self).__init__(message=message)
