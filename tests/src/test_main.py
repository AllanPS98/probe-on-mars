import unittest
from unittest.mock import patch
from src.main import run

class TestMain(unittest.TestCase):
    @patch("uvicorn.run")
    def test_run_function(self, mock_run):
        run()
        mock_run.assert_called_once_with(
            "app:app",
            host="0.0.0.0",
            port=8000,
            limit_concurrency=4,
        )