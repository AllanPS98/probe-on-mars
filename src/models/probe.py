from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Direction(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

class Probe(BaseModel):
    __tablename__ = "probes"

    mesh_id = Column(UUID(as_uuid=True), ForeignKey('meshs.id', ondelete="CASCADE"), nullable=False)
    x_position = Column(Integer, nullable=False, default=0)
    y_position = Column(Integer, nullable=False, default=0)
    direction = Column(String, nullable=False, default=Direction.NORTH.value)

    meshs = relationship("Mesh", back_populates="probes")

    def get(self):
        return {
            "id": str(self.id),
            "x": self.x_position,
            "y": self.y_position,
            "direction": self.direction
        }