import unittest
from uuid import uuid4
from src.models.probe import Probe


class TestProbeModel(unittest.TestCase):

    def test_get(self):
        
        control_process = Probe(
            id=uuid4(),
            x_position=5,
            y_position=5,
            direction="NORTH"
        )
        result = control_process.get()
        self.assertIsInstance(result["id"], str)
        self.assertEqual(result["x"], 5)
        self.assertEqual(result["y"], 5)
        self.assertEqual(result["direction"], "NORTH")