import unittest
from unittest.mock import MagicMock, patch

from src.databases.probe import ProbeDatabase

class TestProbeDatabase(unittest.TestCase):

    @patch("src.databases.mesh.Session")
    def test_insert(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = ProbeDatabase(mock_session.return_value)
        database.insert(MagicMock())

        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called_once()
    
    @patch("src.databases.mesh.Session")
    def test_get_by_id(self, mock_session):
        mock_probe = MagicMock()
        mock_probe.get.return_value = {
            "id": "test_id_1",
            "x": 1,
            "y": 1,
            "direction": "EAST"
        }
        mock_session_instance = MagicMock()
        mock_session_instance.query().filter().options().first.return_value = mock_probe
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = ProbeDatabase(mock_session.return_value)
        probe = database.get_by_id("test_id")
        result = probe.get()

        mock_session_instance.query().filter().options().first.assert_called_once()
        self.assertEqual(result["id"], "test_id_1")
        self.assertEqual(result["x"], 1)
        self.assertEqual(result["y"], 1)
        self.assertEqual(result["direction"], "EAST")
    
    @patch("src.databases.mesh.Session")
    def test_get_all(self, mock_session):
        mock_first_probe = MagicMock()
        mock_first_probe.get.return_value = {
            "id": "test_id_1",
            "x": 1,
            "y": 1,
            "direction": "EAST"
        }
        mock_second_probe = MagicMock()
        mock_second_probe.get.return_value = {
            "id": "test_id_2",
            "x": 3,
            "y": 4,
            "direction": "NORTH"
        }
        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value = [mock_first_probe, mock_second_probe]
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = ProbeDatabase(mock_session.return_value)
        probes = database.get_all()
        first_result = probes[0].get()
        second_result = probes[1].get()

        mock_session_instance.query.assert_called_once()
        self.assertEqual(len(probes), 2)
        self.assertEqual(first_result["id"], "test_id_1")
        self.assertEqual(first_result["x"], 1)
        self.assertEqual(first_result["y"], 1)
        self.assertEqual(first_result["direction"], "EAST")
        self.assertEqual(second_result["id"], "test_id_2")
        self.assertEqual(second_result["x"], 3)
        self.assertEqual(second_result["y"], 4)
        self.assertEqual(second_result["direction"], "NORTH")

    @patch("src.databases.mesh.Session")
    def test_update(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        database = ProbeDatabase(mock_session.return_value)
        database.update("test_id", {"test": "test"})

        mock_session_instance.query().filter().update.assert_called_once()
        mock_session_instance.commit.assert_called_once()
        