import unittest
import pytest
from unittest.mock import patch, MagicMock
from src.databases import get_database_session, get_session


class TestSession(unittest.TestCase):

    @patch("src.databases.create_engine")
    @patch("src.databases.sessionmaker")
    def test_get_database_session_returns_session(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value.return_value = mock_session

        session = get_database_session()

        self.assertEqual(session, mock_session)
        mock_create_engine.assert_called_once()
        mock_sessionmaker.assert_called_once()
    
    @patch("src.databases.logger")
    @patch("src.databases.create_engine")
    @patch("src.databases.sessionmaker")
    def test_get_database_exception(self, mock_sessionmaker, mock_create_engine, mock_logger):
        mock_session = MagicMock()
        mock_sessionmaker.return_value.return_value = mock_session

        with self.assertRaises(RuntimeError):
            with get_session() as session:
                raise RuntimeError("Simulated DB error")

        mock_logger.exception.assert_called_once()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
