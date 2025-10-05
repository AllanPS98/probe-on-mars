import unittest
from unittest.mock import patch

from src.databases.database import Database
from src.databases.mesh import MeshDatabase
from src.databases.probe import ProbeDatabase

class TestDatabase(unittest.TestCase):

    @patch("src.databases.database.get_database_session")
    def test_database(self, mock_session):
        database = Database()
        mock_session.assert_called_once()
        self.assertIsInstance(database.meshs, MeshDatabase)
        self.assertIsInstance(database.probes, ProbeDatabase)