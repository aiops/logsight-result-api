import logging.config
from http import HTTPStatus
from pathlib import Path

import logcheck
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from responses.responses import ErrorResponse
from result_api.dto import VerificationDTO, LogWriterDTO
from result_api.log_verification.verification import LogVerification, NotFoundException
from logsight.services.service_provider import ServiceProvider
from logsight.logger.configuration import LogConfig
from logcheck import log_recommendation

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


@app.post('/api/v1/writer')
def get_recommendations(request: LogWriterDTO):
    settings = logcheck.Settings
    settings.path = Path("")
    settings.language = request.language
    settings.output = Path("")
    settings.debug = False
    settings.zhenhao = False
    settings.alt = True
    settings.probability = 0.95
    try:
        result = log_recommendation(request.code, settings)
    except NotFoundException as e:
        return JSONResponse(content=ErrorResponse(str(e)),
                            status_code=HTTPStatus.NOT_FOUND)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
