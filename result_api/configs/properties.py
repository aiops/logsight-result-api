import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from logsight.configs.properties import ConfigProperties


@ConfigProperties(prefix="result_api",
                  path=Path(os.path.dirname(os.path.realpath(__file__))) / "result_api_config.cfg")
class ResultApiConfig(BaseModel):
    verification_risk_threshold: Optional[int] = 80
