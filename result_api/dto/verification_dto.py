from typing import Dict

from pydantic import BaseModel


class VerificationDTO(BaseModel):
    applicationId: str
    applicationName: str
    baselineTags: str
    privateKey: str
    candidateTags: str
