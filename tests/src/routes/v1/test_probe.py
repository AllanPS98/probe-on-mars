import json
import unittest
from fastapi import Response, status
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.configurations import Configurations
from src.app import app

class TestProbeEndpoints(unittest.TestCase):

    def setUp(self):
        self.configurations = Configurations()
        self.media_type = self.configurations.MEDIA_TYPE
        self.client = TestClient(app)

    @patch("src.routes.v1.probe.ProbeController")
    def test_move(self, mock_controller):
        mock_payload = {
            "probe_id": "test_id",
            "movements": ["M"]
        }
        mock_content = json.dumps({
            "id": "test_id",
            "x": 1,
            "y": 1,
            "direction": "EAST"
        })
        mock_response = Response(
            content=mock_content,
            media_type=self.media_type,
            status_code=status.HTTP_200_OK
        )
        mock_controller().move.return_value = mock_response
        response = self.client.post("/v1/probe/move", json=mock_payload)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["id"], "test_id")
        self.assertEqual(data["x"], 1)
        self.assertEqual(data["y"], 1)
        self.assertEqual(data["direction"], "EAST")
    
    @patch("src.routes.v1.probe.ProbeController")
    def test_get_all(self, mock_controller):
        mock_content = json.dumps({
            "probes": [
                {
                    "id": "test_id_1",
                    "x": 1,
                    "y": 1,
                    "direction": "EAST"
                },
                {
                    "id": "test_id_2",
                    "x": 3,
                    "y": 4,
                    "direction": "NORTH"
                }
            ]
        })
        mock_response = Response(
            content=mock_content,
            media_type=self.media_type,
            status_code=status.HTTP_200_OK
        )
        mock_controller().get_all.return_value = mock_response
        response = self.client.get("/v1/probe")
        data = response.json()
        first_probe = data["probes"][0]
        second_probe = data["probes"][1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(first_probe["id"], "test_id_1")
        self.assertEqual(first_probe["x"], 1)
        self.assertEqual(first_probe["y"], 1)
        self.assertEqual(first_probe["direction"], "EAST")
        self.assertEqual(second_probe["id"], "test_id_2")
        self.assertEqual(second_probe["x"], 3)
        self.assertEqual(second_probe["y"], 4)
        self.assertEqual(second_probe["direction"], "NORTH")