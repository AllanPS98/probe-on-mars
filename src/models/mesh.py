import enum
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Mesh(BaseModel):
    __tablename__ = "meshs"

    x_limit = Column(Integer, nullable=False)
    y_limit = Column(Integer, nullable=False)

    probes = relationship("Probe", back_populates="meshs", cascade="all, delete-orphan")
    
    def get(self):
        return {
            "x_limit": self.x_limit,
            "y_limit": self.y_limit,
        }