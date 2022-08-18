import logging.config
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from responses.responses import ErrorResponse
from result_api.dto import VerificationDTO
from result_api.log_verification.verification import LogVerification, NotFoundException
from logsight.services.service_provider import ServiceProvider
from logsight.logger.configuration import LogConfig

app = FastAPI()


logging.config.dictConfig(LogConfig().config)
logger = logging.getLogger('logsight')


@app.post('/api/v1/compare')
def get_tasks(request: VerificationDTO):
    try:
        result = LogVerification(ServiceProvider.provide_elasticsearch()).run_verification(
            private_key=request.privateKey,
            baseline_tags=request.baselineTags,
            candidate_tags=request.candidateTags)
    except NotFoundException as e:
        return JSONResponse(content=ErrorResponse(str(e)),
                            status_code=HTTPStatus.NOT_FOUND)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
