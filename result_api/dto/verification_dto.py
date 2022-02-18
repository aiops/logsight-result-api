from pydantic import BaseModel


class VerificationDTO(BaseModel):
    applicationId: str
    applicationName: str
    baselineTag: str
    privateKey: str
    compareTag: str
