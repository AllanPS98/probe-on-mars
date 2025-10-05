import json
import unittest
from unittest.mock import MagicMock, patch

from src.controllers.mesh import MeshController


class TestMeshController(unittest.TestCase):

    @patch("src.controllers.mesh.ProbeController")
    @patch("src.controllers.mesh.Database")
    def test_create(self, mock_database, mock_probe_controller):
        payload = MagicMock()
        payload.x = 5
        payload.y = 5
        payload.direction.value = "NORTH"
        probe_response_mock = {
            "id": "test_id",
            "x": 0,
            "y": 0,
            "direction": "NORTH"
        }
        mock_probe_controller().create.return_value = probe_response_mock
        response = MeshController().create(payload)
        result = json.loads(response.body)

        mock_database().meshs.insert.assert_called_once()
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "NORTH")
    
    @patch("src.controllers.mesh.ProbeController")
    @patch("src.controllers.mesh.Database")
    def test_create_error(self, mock_database, mock_probe_controller):
        payload = MagicMock()
        payload.x = 5
        payload.y = 5
        payload.direction.value = "NORTH"
        mock_probe_controller().create.side_effect = Exception("test")
        
        response = MeshController().create(payload)

        mock_database().meshs.insert.assert_called_once()
        self.assertEqual(response.status_code, 500)
    
    @patch("src.controllers.mesh.ProbeController")
    @patch("src.controllers.mesh.Database")
    def test_create_not_probe_response(self, mock_database, mock_probe_controller):
        payload = MagicMock()
        payload.x = 5
        payload.y = 5
        payload.direction.value = "NORTH"
        mock_probe_controller().create.return_value = {}
        
        response = MeshController().create(payload)

        mock_database().meshs.insert.assert_called_once()
        self.assertEqual(response.status_code, 500)