from fastapi import Response, status
from src.configurations import Configurations
from src.databases.database import Database
from src.models.probe import Probe
from src.schemas.probe import GetProbes, MoveProbePayload, ProbeResponse

configurations = Configurations()


class ProbeController:

    @property
    def __database(self) -> Database:
        return Database()
    
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

    def create(self, mesh_id: str):
        probe_instance = Probe(
            mesh_id=mesh_id
        )
        self.__database.probes.insert(probe_instance)
