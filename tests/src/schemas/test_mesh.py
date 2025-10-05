import unittest

from src.models.probe import Direction
from src.schemas.mesh import CreateMeshPayload


class TestMeshSchema(unittest.TestCase):

    def test_validate_coordenates(self):
        with self.assertRaises(ValueError):
            CreateMeshPayload(
                x=1,
                y=0,
                direction=Direction.NORTH
            )