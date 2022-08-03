from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from result_api.dto import VerificationDTO
from result_api.log_verification.verification import LogVerification
from logsight.services.service_provider import ServiceProvider

app = FastAPI()


@app.post('/api/v1/compare')
def get_tasks(request: VerificationDTO):
    result = LogVerification(ServiceProvider.provide_elasticsearch()).run_verification(
        private_key=request.privateKey,
        baseline_tags=request.baselineTags,
        candidate_tags=request.candidateTags)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)
