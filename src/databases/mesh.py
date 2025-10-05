from sqlalchemy.orm import Session

from src.models.mesh import Mesh


class MeshDatabase:

    def __init__(self, database_session: Session):
        self.database_session = database_session
    
    def insert(self, instance: Mesh):
        with self.database_session as session:
            session.add(instance)
            session.commit()
    
    def delete(self, mesh_id: str):
        with self.database_session as session:
            session.query(Mesh).filter(Mesh.id == mesh_id).delete()
            session.commit()