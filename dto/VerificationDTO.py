from pydantic import BaseModel


class VerificationDTO(BaseModel):
    applicationName: str
    baselineTag: str
    privateKey: str
    compareTag: str
