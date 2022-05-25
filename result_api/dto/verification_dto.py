from typing import Dict

from pydantic import BaseModel


class VerificationDTO(BaseModel):
    baselineTags: str
    privateKey: str
    candidateTags: str
