import unittest
from src.app import app

class TestApp(unittest.TestCase):

    def test_app_initialization(self):
        routes = [route.path for route in app.routes]

        self.assertIsNotNone(app.title)
        self.assertIsNotNone(app.version)
        self.assertIn("/health-check", routes)
        self.assertIn("/v1/mesh/create", routes)
        self.assertIn("/v1/probe/move", routes)
        self.assertIn("/v1/probe", routes)