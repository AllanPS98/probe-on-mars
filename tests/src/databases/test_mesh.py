import unittest
from unittest.mock import MagicMock, patch

from src.databases.mesh import MeshDatabase

class TestMeshDatabase(unittest.TestCase):

    @patch("src.databases.mesh.Session")
    def test_insert(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = MeshDatabase(mock_session.return_value)
        database.insert(MagicMock())

        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called_once()
    
    @patch("src.databases.mesh.Session")
    def test_delete(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = MeshDatabase(mock_session.return_value)
        database.delete("test_id")

        mock_session_instance.query().filter().delete.assert_called_once()
        mock_session_instance.commit.assert_called_once()
        