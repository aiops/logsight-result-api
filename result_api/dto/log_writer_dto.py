from pydantic import BaseModel


class LogWriterDTO(BaseModel):
    code: str
    language: str
