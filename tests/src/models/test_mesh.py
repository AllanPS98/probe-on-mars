import unittest
from uuid import uuid4
from src.models.mesh import Mesh


class TestMeshModel(unittest.TestCase):

    def test_get(self):
        
        control_process = Mesh(
            x_limit=5,
            y_limit=5
        )
        result = control_process.get()
        self.assertEqual(result["x_limit"], 5)
        self.assertEqual(result["y_limit"], 5)