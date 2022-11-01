from typing import Dict, Union

from pydantic import BaseModel


class AutologDTO(BaseModel):
    code: str
    language: str
