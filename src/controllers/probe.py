from typing import Dict, Tuple
from fastapi import Response, status
from loguru import logger
from src.configurations import Configurations
from src.databases.database import Database
from src.models.probe import Probe, Direction
from src.schemas.probe import GetProbes, MoveProbePayload, ProbeResponse, Movement

configurations = Configurations()


class ProbeController:

    @property
    def __database(self) -> Database:
        return Database()
    
    def __direction_rules(self, movement: str, current_direction: str) -> str:
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
        new_direction = rules.get(movement).get(current_direction)
        return new_direction
    
    def __movement_rules(self, current_x: int, current_y: int, x_limit: int, y_limit: int, current_direction: str) -> Dict:
        rules = {
            Direction.NORTH.value: [current_x, current_y+1],
            Direction.SOUTH.value: [current_x, current_y-1],
            Direction.EAST.value: [current_x+1, current_y],
            Direction.WEST.value: [current_x-1, current_y]
        }
        new_position = rules.get(current_direction)
        if new_position[0] < 0 or new_position[0] > x_limit:
            return {"x": current_x, "y": current_y}
        if new_position[1] < 0 or new_position[1] > y_limit:
            return {"x": current_x, "y": current_y}
        return {"x": new_position[0], "y": new_position[1]}
    
    def move(self, payload: MoveProbePayload) -> Response:
        pass

    def get_all(self) -> Response:
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

    def create(self, mesh_id: str) -> Dict:
        try:
            probe_instance = Probe(
                mesh_id=mesh_id
            )
            self.__database.probes.insert(probe_instance)
            return probe_instance.get()
        except Exception as exception:
            logger.exception(f"Error in create mesh method: {exception}")
            return {}
