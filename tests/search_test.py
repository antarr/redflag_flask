import unittest
from unittest.mock import MagicMock, patch
from api.models.twitter import Twitter
import vcr


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

    def test_search_success_with_images(self):
        with vcr.use_cassette('tests/fixtures/search_success_with_images.yaml'):
            term = 'test'
            response = Twitter().search(term)
            expected = '3_1619751159371280385'
            self.assertEqual(response['images'][0]['key'], expected)

    def test_image_classifier(self):
        file_path = 'images/doll.jpg'
        classifications = Twitter().classify_image(file_path)
        self.assertIsNotNone(classifications[0]['prediction'])
