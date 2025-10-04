from fastapi import Response
from src.databases.database import Database
from src.schemas.mesh import CreateMeshPayload


class MeshController:

    @property
    def __database(self) -> Database:
        return Database()
    
    def create(self, payload: CreateMeshPayload) -> Response:
        pass
