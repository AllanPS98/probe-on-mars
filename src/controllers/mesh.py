from typing import Dict
from fastapi import Response, status
from loguru import logger
from src.configurations import Configurations
from src.controllers.probe import ProbeController
from src.databases.database import Database
from src.models.mesh import Mesh
from src.schemas.mesh import CreateMeshPayload, CreateMeshError
from src.schemas.probe import ProbeResponse

configurations = Configurations()

class MeshController:

    @property
    def __database(self) -> Database:
        return Database()

    @property
    def __probe_controller(self) -> ProbeController:
        return ProbeController()
    
    def __creating_mesh_error(self, mesh_id: str) -> Response:
        self.__database.meshs.delete(mesh_id)
        error_schema = CreateMeshError(
            message="error when creating probe"
        )
        return self.__response_error(error_schema)

    def __response_error(self, error_schema: CreateMeshError) -> Response:
        response_error = Response(
            content=error_schema.model_dump_json(),
            media_type=configurations.MEDIA_TYPE,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return response_error
    
    def __creating_mesh_success(self, probe_response: Dict) -> Response:
        probe_schema = ProbeResponse(
            id=probe_response.get("id"),
            x=probe_response.get("x"),
            y=probe_response.get("y"),
            direction=probe_response.get("direction")
        )
        response = Response(
            content=probe_schema.model_dump_json(),
            media_type=configurations.MEDIA_TYPE,
            status_code=status.HTTP_201_CREATED
        )
        
        return response
    
    def create(self, payload: CreateMeshPayload) -> Response:
        try:
            mesh_instance = Mesh(
                x_limit=payload.x,
                y_limit=payload.y
            )
            self.__database.meshs.insert(mesh_instance)
            probe_response = self.__probe_controller.create(mesh_instance.id, payload.direction.value)
            if not probe_response:
                response_error = self.__creating_mesh_error(mesh_instance.id)
                return response_error
            response = self.__creating_mesh_success(probe_response)
            return response
        except Exception as exception:
            logger.exception(f"Error when creating mesh: {exception}")
            error_schema = CreateMeshError(
                message="error when creating mesh"
            )
            return self.__response_error(error_schema)


