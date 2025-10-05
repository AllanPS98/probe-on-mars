from src.databases import get_database_session
from src.databases.mesh import MeshDatabase
from src.databases.probe import ProbeDatabase


class Database:

    def __init__(self):
        self.database_session = get_database_session()
    
    @property
    def meshs(self) -> MeshDatabase:
        return MeshDatabase(self.database_session)
    
    @property
    def probes(self) -> ProbeDatabase:
        return ProbeDatabase(self.database_session)
