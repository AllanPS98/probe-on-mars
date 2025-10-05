from enum import Enum
from typing import List
from pydantic import BaseModel, field_validator
from loguru import logger

class Movement(Enum):
    MOVE = "M"
    RIGHT = "R"
    LEFT = "L"

class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: str

class ProbeResponseError(BaseModel):
    message: str

class MoveProbePayload(BaseModel):
    probe_id: str
    movements: List[Movement]

class GetProbes(BaseModel):
    probes: List[ProbeResponse]