import unittest
from unittest.mock import patch

from tracker import Carrier
from tracker.fetch_status import (
    fetch_status,
    fetch_ups_status,
    fetch_fedex_status,
    fetch_usps_status,
    fetch_dhl_status,
    fetch_amazon_status,
)


class FetchStatusTests(unittest.TestCase):
    @patch('tracker.http_client.get_json')
    def test_fetch_ups_status(self, mock_get):
        mock_get.return_value = {
            'status': 'Delivered',
            'estimated_delivery': '2025-01-01',
            'current_location': 'Somewhere'
        }
        result = fetch_ups_status('1Z999')
        self.assertEqual(result['status'], 'Delivered')
        self.assertEqual(result['estimated_delivery'], '2025-01-01')
        self.assertEqual(result['current_location'], 'Somewhere')

    @patch('tracker.http_client.get_json')
    def test_fetch_status_router(self, mock_get):
        mock_get.return_value = {
            'status': 'Shipped',
            'estimated_delivery': '2025-01-02',
            'current_location': 'Town'
        }
        result = fetch_status(Carrier.DHL, '123')
        self.assertEqual(result['status'], 'Shipped')


if __name__ == '__main__':
    unittest.main()

