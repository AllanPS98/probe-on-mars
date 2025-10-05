import unittest
from src.configurations import Configurations

class TestApplicationConfig(unittest.TestCase):

    def test_config(self):
        
        configurations = Configurations()
        self.assertEqual("0.0.0.0", configurations.APP_HOST)
        self.assertEqual(8000, configurations.APP_PORT)
        self.assertEqual("Probe on Mars", configurations.APP_NAME)
        self.assertEqual("1.0.0", configurations.APP_VERSION)
        self.assertEqual("postgres", configurations.DB_USERNAME)
        self.assertEqual("postgres", configurations.DB_PASSWORD)
        self.assertEqual("postgres", configurations.DB_NAME)
        self.assertEqual("localhost", configurations.DB_HOST)
        self.assertEqual("5432", configurations.DB_PORT)
        self.assertIn('postgresql+psycopg2://', configurations.DB_STRING_URI)
        self.assertEqual("application/json", configurations.MEDIA_TYPE)
        