from fastapi import APIRouter, status
from src.controllers.probe import ProbeController
from src.schemas.probe import GetProbes, MoveProbePayload, ProbeResponse

router = APIRouter(prefix="/probe")

@router.post(
    "/move",
    response_model=ProbeResponse,
    status_code=status.HTTP_200_OK
)
def move_probe(payload: MoveProbePayload):
    return ProbeController().move(payload) 

@router.get(
    "",
    response_model=GetProbes,
    status_code=status.HTTP_200_OK
)
def get_probes():
    return ProbeController().get_all()