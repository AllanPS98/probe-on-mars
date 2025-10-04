from sqlalchemy.orm import Session


class MeshDatabase:

    def __init__(self, database_session: Session):
        self.database_session = database_session