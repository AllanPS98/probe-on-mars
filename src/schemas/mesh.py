from pydantic import BaseModel

class CreateMeshPayload(BaseModel):
    x: int
    y: int
    direction: str

class CreateMeshError(BaseModel):
    message: str
