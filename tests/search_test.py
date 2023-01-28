import unittest
from unittest.mock import MagicMock, patch
from api.models.twitter import Twitter


class SearchTest(unittest.TestCase):
    @patch('requests.get', return_value=MagicMock(status_code=401))
    def test_search_unauthorized(self, mock_get):
        term = 'test'
        response = Twitter().search(term)
        expected = {
            "images": [],
            "query": "test",
            "status_code": 401,
            "status_text": "Invalid Bearer Token"
        }
        self.assertEqual(response, expected)

    @patch('requests.get', return_value=MagicMock(status_code=429))
    def test_search_rate_limit(self, mock_get):
        term = 'test'
        response = Twitter().search(term)
        expected = {
            "images": [],
            "query": "test",
            "status_code": 429,
            "status_text": "Rate limit exceeded"
        }
        self.assertEqual(response, expected)

    @patch('requests.get', return_value=MagicMock(status_code=500))
    def test_search_internal_server_error(self, mock_get):
        term = 'test'
        response = Twitter().search(term)
        expected = {
            "images": [],
            "query": "test",
            "status_code": 500,
            "status_text": "Internal Server Error"
        }
        self.assertEqual(response, expected)

    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_search_success_with_images(self, mock_get):
        term = 'test'
        mock_get.return_value.json.return_value = {
            "data": [
                {
                    "attachments": {
                        "media_keys": [
                            "test"
                        ],
                        "media": {
                            "test": {
                                "url": "test"
                            }
                        }
                    },
                    "text": "test"
                }
            ]
        }
        response = Twitter().search(term)
        expected = {
            "images": [
                {
                    "tweet": "test",
                    "url": "test"
                }
            ],
            "query": "test",
            "status_code": 200,
            "status_text": "OK"
        }
        self.assertEqual(response, expected)

    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_exception(self, mock_get):
        term = 'test'
        with patch('requests.get', side_effect=Exception):
            response = Twitter().search(term)
            expected = {
                "images": [],
                "query": "test",
                "status_code": 500,
                "status_text": "Internal Server Error"
            }
            self.assertEqual(response, expected)
