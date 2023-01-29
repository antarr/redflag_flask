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
            "includes": {
                "media": [
                    {
                        "url": "https://pbs.twimg.com/media/FnmRzMEX0AQjDvl.jpg",
                        "media_key": "3_1619485849615323140",
                        "type": "photo"
                    },
                    {
                        "url": "https://pbs.twimg.com/media/FnmRrwnXoAEzkUO.jpg",
                        "media_key": "3_1619485721986834433",
                        "type": "photo"
                    }]
            }
        }
        response = Twitter().search(term)
        expected = {
            "images": [
                {
                    "key": "3_1619485849615323140",
                    "url": "https://pbs.twimg.com/media/FnmRzMEX0AQjDvl.jpg"
                },
                {
                    "key": "3_1619485721986834433",
                    "url": "https://pbs.twimg.com/media/FnmRrwnXoAEzkUO.jpg"
                }
            ],
            "query": "test",
            "status_code": 200,
            "status_text": "OK"
        }
        self.assertEqual(response, expected)
