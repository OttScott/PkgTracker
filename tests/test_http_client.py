import unittest
from unittest.mock import patch, MagicMock

import requests

from tracker.http_client import get_json


class HttpClientTests(unittest.TestCase):
    @patch('requests.get')
    def test_get_json_success(self, mock_get):
        response = MagicMock()
        response.json.return_value = {'hello': 'world'}
        response.status_code = 200
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        data = get_json('http://example.com')
        self.assertEqual(data, {'hello': 'world'})

    @patch('requests.get', side_effect=requests.RequestException('boom'))
    def test_get_json_error(self, mock_get):
        data = get_json('http://example.com')
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()

