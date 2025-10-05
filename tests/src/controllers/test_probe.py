import json
import unittest
from unittest.mock import MagicMock, patch

from src.controllers.probe import ProbeController
from src.schemas.probe import Movement


class TestProbeController(unittest.TestCase):

    @patch("src.controllers.probe.Database")
    def test_create(self, mock_database):
        result = ProbeController().create(mesh_id="test_id", direction="NORTH")

        mock_database().probes.insert.assert_called_once()
        self.assertEqual(result["direction"], "NORTH")
    
    @patch("src.controllers.probe.Database")
    def test_create_error(self, mock_database):
        mock_database().probes.insert.side_effect = Exception("test")
        
        result = ProbeController().create(mesh_id="test_id", direction="NORTH")

        mock_database().probes.insert.assert_called_once()
        self.assertEqual(result, {})
    
    @patch("src.controllers.probe.Database")
    def test_get_all_error(self, mock_database):
        mock_database().probes.get_all.return_value = Exception("test")
        
        response = ProbeController().get_all()

        mock_database().probes.get_all.assert_called_once()
        self.assertEqual(response.status_code, 500)
    
    @patch("src.controllers.probe.Database")
    def test_get_all(self, mock_database):
        mock_probe = MagicMock()
        mock_probe.get.return_value = {
            "id": "test_id",
            "x": 0,
            "y": 0,
            "direction": "NORTH"
        }
        mock_database().probes.get_all.return_value = [mock_probe]
        
        response = ProbeController().get_all()
        result = json.loads(response.body)["probes"][0]

        mock_database().probes.get_all.assert_called_once()
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "NORTH")
    
    @patch("src.controllers.probe.Database")
    def test_move_up(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 0
        mock_probe.direction = "NORTH"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 1)
        self.assertEqual(result["direction"], "NORTH")

    @patch("src.controllers.probe.Database")
    def test_move_down(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 1
        mock_probe.direction = "SOUTH"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "SOUTH")

    @patch("src.controllers.probe.Database")
    def test_move_left(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 1
        mock_probe.y_position = 0
        mock_probe.direction = "WEST"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "WEST")

    @patch("src.controllers.probe.Database")
    def test_move_right(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 0
        mock_probe.direction = "EAST"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 1)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "EAST")
    
    @patch("src.controllers.probe.Database")
    def test_move_rotate_direction_left(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.LEFT]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 0
        mock_probe.direction = "NORTH"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "WEST")
    
    @patch("src.controllers.probe.Database")
    def test_move_rotate_direction_right(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.RIGHT]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 0
        mock_probe.direction = "EAST"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "SOUTH")
    
    @patch("src.controllers.probe.Database")
    def test_move_x_out_of_limit(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 5
        mock_probe.y_position = 0
        mock_probe.direction = "EAST"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 5)
        self.assertEqual(result["y"], 0)
        self.assertEqual(result["direction"], "EAST")
    
    @patch("src.controllers.probe.Database")
    def test_move_y_out_of_limit(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_mesh = MagicMock()
        mock_mesh.x_limit = 5
        mock_mesh.y_limit = 5
        mock_probe = MagicMock()
        mock_probe.id = "test_id"
        mock_probe.x_position = 0
        mock_probe.y_position = 5
        mock_probe.direction = "NORTH"
        mock_probe.meshs = mock_mesh
        mock_database().probes.get_by_id.return_value = mock_probe
        response = ProbeController().move(payload)
        result = json.loads(response.body)
        self.assertEqual(result["id"], "test_id")
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 5)
        self.assertEqual(result["direction"], "NORTH")
    
    @patch("src.controllers.probe.Database")
    def test_move_not_found(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_database().probes.get_by_id.return_value = None
        response = ProbeController().move(payload)
        self.assertEqual(response.status_code, 404)
    
    @patch("src.controllers.probe.Database")
    def test_move_error(self, mock_database):
        payload = MagicMock()
        payload.probe_id = "test_id"
        payload.movements = [Movement.MOVE]
        mock_database().probes.get_by_id.return_value = Exception("test")
        response = ProbeController().move(payload)
        self.assertEqual(response.status_code, 500)
    