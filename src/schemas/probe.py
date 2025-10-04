from enum import Enum
from typing import List
from pydantic import BaseModel

class Instruction(Enum):
    MOVE = "M"
    RIGHT = "R"
    LEFT = "L"

class ProbeResponse(BaseModel):
    id: str
    x: int
    y: int
    direction: str

class Movement(BaseModel):
    instruction: Instruction

class MoveProbePayload(BaseModel):
    probe_id: str
    movements: List[Movement]

class GetProbes(BaseModel):
    probes: List[ProbeResponse]