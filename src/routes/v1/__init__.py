from fastapi import APIRouter
from src.routes.v1.mesh import router as mesh_router
from src.routes.v1.probe import router as probe_router

v1 = APIRouter(prefix="/v1")
v1.include_router(probe_router, tags=["Probe"])
v1.include_router(mesh_router, tags=["Mesh"])