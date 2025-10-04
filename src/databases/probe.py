from typing import Dict, List
from sqlalchemy.orm import Session

from src.models.probe import Probe


class ProbeDatabase:

    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def insert(self, instance: Probe):
        with self.database_session as session:
            session.add(instance)
            session.commit()
    
    def get_all(self) -> List[Probe]:
        with self.database_session as session:
            probes = session.query(Probe)
            return probes
    
    def update(self, probe_id: str, probe_data: Dict):
        with self.database_session as session:
            session.query(Probe).filter(Probe.id == probe_id).update(probe_data)
            session.commit()