from typing import Dict

from pydantic import BaseModel


class VerificationDTO(BaseModel):
    applicationId: str
    applicationName: str
    baselineTags: Dict[str, str]
    privateKey: str
    candidateTags: Dict[str, str]
