from pydantic import BaseModel, field_validator

from src.models.probe import Direction

class CreateMeshPayload(BaseModel):
    x: int
    y: int
    direction: Direction

    @field_validator("x", "y")
    def validate_coordenates(cls, value):
        if value <= 0:
            raise ValueError("Coordenates must be a positive integer")
        return value

class CreateMeshError(BaseModel):
    message: str
