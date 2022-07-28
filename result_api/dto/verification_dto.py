from typing import Dict, Union

from pydantic import BaseModel


class VerificationDTO(BaseModel):
    baselineTags: Union[str, Dict[str, str]]
    privateKey: str
    candidateTags: Union[str, Dict[str, str]]
