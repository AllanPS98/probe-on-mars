from fastapi import APIRouter, status
from src.controllers.mesh import MeshController
from src.schemas.mesh import CreateMeshPayload
from src.schemas.probe import ProbeResponse

router = APIRouter(prefix="/mesh")

@router.post(
    "/create",
    response_model=ProbeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_mesh(payload: CreateMeshPayload):
    return MeshController().create(payload)
