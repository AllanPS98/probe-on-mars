from typing import Dict, Tuple
from fastapi import Response, status
from loguru import logger
from src.configurations import Configurations
from src.databases.database import Database
from src.models.mesh import Mesh
from src.models.probe import Probe, Direction
from src.schemas.probe import GetProbes, MoveProbePayload, ProbeResponse, Movement, ProbeResponseError

configurations = Configurations()


class ProbeController:

    @property
    def __database(self) -> Database:
        return Database()
    
    def __direction_rules(self, movement: str, current_direction: str) -> Dict:
        rules = {
            Movement.LEFT.value: {
                Direction.NORTH.value: Direction.WEST.value,
                Direction.WEST.value: Direction.SOUTH.value,
                Direction.SOUTH.value: Direction.EAST.value,
                Direction.EAST.value: Direction.NORTH.value
            },
            Movement.RIGHT.value: {
                Direction.NORTH.value: Direction.EAST.value,
                Direction.EAST.value: Direction.SOUTH.value,
                Direction.SOUTH.value: Direction.WEST.value,
                Direction.WEST.value: Direction.NORTH.value
            }
        }
        new_direction = rules.get(movement, {}).get(current_direction, current_direction)
        return {"direction": new_direction}
    
    def __movement_rules(self, movement: str, current_x: int, current_y: int, x_limit: int, y_limit: int, current_direction: str) -> Dict:
        rules = {
            Movement.MOVE.value: {
                Direction.NORTH.value: [current_x, current_y+1],
                Direction.SOUTH.value: [current_x, current_y-1],
                Direction.EAST.value: [current_x+1, current_y],
                Direction.WEST.value: [current_x-1, current_y]
            }
        }
        new_var = rules.get(movement, {})
        new_position = new_var.get(current_direction, [current_x, current_y])
        if new_position[0] < 0 or new_position[0] > x_limit:
            return {"x_position": current_x, "y_position": current_y}
        if new_position[1] < 0 or new_position[1] > y_limit:
            return {"x_position": current_x, "y_position": current_y}
        return {"x_position": new_position[0], "y_position": new_position[1]}

    def __not_found_probe(self, payload: MoveProbePayload) -> Response:
        logger.error(f"Probe instance with id: {payload.probe_id} not found")
        error_schema = ProbeResponseError(message="probe not found")
        response = Response(
            content=error_schema.model_dump_json(), 
            media_type=configurations.MEDIA_TYPE,
            status_code=status.HTTP_404_NOT_FOUND
        )
        return response

    def __execute_movements(self, payload: MoveProbePayload, mesh_instance: Mesh, probe_id: str):
        for movement in payload.movements:
            probe_instance = self.__database.probes.get_by_id(payload.probe_id)
            instruction = movement.value
            current_x = probe_instance.x_position
            current_y = probe_instance.y_position
            current_direction = probe_instance.direction
            x_limit = mesh_instance.x_limit
            y_limit = mesh_instance.y_limit
            new_positions = self.__movement_rules(
                movement=instruction,
                current_x=current_x,
                current_y=current_y,
                x_limit=x_limit,
                y_limit=y_limit,
                current_direction=current_direction,
            )
            new_direction = self.__direction_rules(
                movement=instruction,
                current_direction=current_direction
            )
            new_positions.update(new_direction)
            self.__database.probes.update(probe_id=probe_id, probe_data=new_positions)
        return new_positions
    
    def move(self, payload: MoveProbePayload) -> Response:
        probe_instance = self.__database.probes.get_by_id(payload.probe_id)
        if not probe_instance:
            return self.__not_found_probe(payload)
        try:
            mesh_instance = probe_instance.meshs
            probe_id = str(probe_instance.id)
            new_positions = self.__execute_movements(payload, mesh_instance, probe_id)
            probe_schema = ProbeResponse(
                id=probe_id,
                x=new_positions.get("x_position"),
                y=new_positions.get("y_position"),
                direction=new_positions.get("direction")
            )
            response = Response(
                content=probe_schema.model_dump_json(),
                media_type=configurations.MEDIA_TYPE,
                status_code=status.HTTP_200_OK
            )
            return response
        except Exception as exception:
            logger.exception(f"Error in move probe method: {exception}")
            error_schema = ProbeResponseError(message="move probe failed")
            response = Response(
                content=error_schema.model_dump_json(), 
                media_type=configurations.MEDIA_TYPE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return response

    def get_all(self) -> Response:
        try:
            probes = self.__database.probes.get_all()
            probes_schema = []
            for probe in probes:
                probe_schema = ProbeResponse(**probe.get())
                probes_schema.append(probe_schema)

            get_probes_schema = GetProbes(probes=probes_schema)
            response = Response(
                content=get_probes_schema.model_dump_json(), 
                media_type=configurations.MEDIA_TYPE,
                status_code=status.HTTP_200_OK
            )
            return response
        except Exception as exception:
            logger.exception(f"Error in get all probes method: {exception}")
            error_schema = ProbeResponseError(message="get all probes failed")
            response = Response(
                content=error_schema.model_dump_json(), 
                media_type=configurations.MEDIA_TYPE,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return response

    def create(self, mesh_id: str, direction: str) -> Dict:
        try:
            probe_instance = Probe(
                mesh_id=mesh_id,
                direction=direction
            )
            self.__database.probes.insert(probe_instance)
            return probe_instance.get()
        except Exception as exception:
            logger.exception(f"Error in create probe method: {exception}")
            return {}
