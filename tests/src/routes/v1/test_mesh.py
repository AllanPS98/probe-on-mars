import json
import unittest
from fastapi import Response, status
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.configurations import Configurations
from src.app import app

class TestMeshEndpoints(unittest.TestCase):

    def setUp(self):
        self.configurations = Configurations()
        self.media_type = self.configurations.MEDIA_TYPE
        self.client = TestClient(app)

    @patch("src.routes.v1.mesh.MeshController")
    def test_create(self, mock_controller):
        mock_payload = {
            "x": 5,
            "y": 5,
            "direction": "NORTH"
        }
        mock_content = json.dumps({
            "id": "test_id",
            "x": 5,
            "y": 5,
            "direction": "NORTH"
        })
        mock_response = Response(
            content=mock_content,
            media_type=self.media_type,
            status_code=status.HTTP_201_CREATED
        )
        mock_controller().create.return_value = mock_response
        response = self.client.post("/v1/mesh/create", json=mock_payload)
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["id"], "test_id")
        self.assertEqual(data["x"], 5)
        self.assertEqual(data["y"], 5)
        self.assertEqual(data["direction"], "NORTH")