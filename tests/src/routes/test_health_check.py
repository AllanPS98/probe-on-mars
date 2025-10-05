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
    
    def test_get_all(self):
        response = self.client.get("/health-check")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "ok")