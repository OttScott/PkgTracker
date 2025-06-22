"""
Tests for the HTTP client module.
"""
import unittest
from unittest.mock import patch, Mock
from tracker.carriers import Carrier
from tracker.http_client import (
    HTTPClient, UPSClient, FedExClient, USPSClient, DHLClient, AmazonClient,
    APIError, RequestMethod, get_client_for_carrier
)

class TestHTTPClient(unittest.TestCase):
    """Test the HTTPClient class."""

    @patch("os.getenv")
    def test_get_ups_credentials(self, mock_getenv):
        """Test getting UPS credentials."""
        mock_getenv.side_effect = lambda key, default: {
            "UPS_API_KEY": "test-api-key",
            "UPS_CLIENT_ID": "test-client-id",
            "UPS_CLIENT_SECRET": "test-client-secret"
        }.get(key, default)
        
        credentials = HTTPClient.get_ups_credentials()
        
        self.assertEqual(credentials["api_key"], "test-api-key")
        self.assertEqual(credentials["client_id"], "test-client-id")
        self.assertEqual(credentials["client_secret"], "test-client-secret")
    
    @patch("os.getenv")
    def test_get_fedex_credentials(self, mock_getenv):
        """Test getting FedEx credentials."""
        mock_getenv.side_effect = lambda key, default: {
            "FEDEX_API_KEY": "test-api-key",
            "FEDEX_ACCOUNT_NUMBER": "test-account-number",
            "FEDEX_METER_NUMBER": "test-meter-number"
        }.get(key, default)
        
        credentials = HTTPClient.get_fedex_credentials()
        
        self.assertEqual(credentials["api_key"], "test-api-key")
        self.assertEqual(credentials["account_number"], "test-account-number")
        self.assertEqual(credentials["meter_number"], "test-meter-number")
    
    @patch("requests.request")
    def test_make_request_successful(self, mock_request):
        """Test making a successful HTTP request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_request.return_value = mock_response
        
        response = HTTPClient.make_request(
            method=RequestMethod.GET,
            url="https://test.com/api",
            headers={"X-Test": "test"}
        )
        
        self.assertEqual(response, {"data": "test"})
        mock_request.assert_called_once_with(
            method="GET",            url="https://test.com/api",
            headers={"X-Test": "test"},
            params={},
            data=None,
            timeout=30,
            verify=True
        )
    
    @patch("requests.request")
    def test_make_request_http_error(self, mock_request):
        """Test handling of HTTP errors."""
        from requests.exceptions import HTTPError
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not found"}
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        mock_request.return_value = mock_response
        
        with self.assertRaises(APIError) as context:
            HTTPClient.make_request(
                method=RequestMethod.GET,
                url="https://test.com/api"
            )
        
        self.assertIn("HTTP error", str(context.exception))


class TestCarrierClients(unittest.TestCase):
    """Test the carrier-specific API clients."""
    
    @patch("tracker.http_client.HTTPClient.make_request")
    @patch("tracker.http_client.HTTPClient.get_ups_credentials")
    def test_ups_client(self, mock_get_credentials, mock_make_request):
        """Test the UPS client."""
        mock_get_credentials.return_value = {
            "api_key": "test-api-key",
            "client_id": "test-client-id",
            "client_secret": "test-client-secret"
        }
        mock_make_request.return_value = {"data": "test"}
        
        response = UPSClient.get_tracking_info("1Z999AA10123456784")
        
        self.assertEqual(response, {"data": "test"})
        mock_make_request.assert_called_once()
        self.assertEqual(mock_make_request.call_args[1]["method"], RequestMethod.GET)
    
    @patch("tracker.http_client.HTTPClient.make_request")
    @patch("tracker.http_client.HTTPClient.get_fedex_credentials")
    def test_fedex_client(self, mock_get_credentials, mock_make_request):
        """Test the FedEx client."""
        mock_get_credentials.return_value = {
            "api_key": "test-api-key",
            "account_number": "test-account-number",
            "meter_number": "test-meter-number"
        }
        mock_make_request.return_value = {"data": "test"}
        
        response = FedExClient.get_tracking_info("123456789012")
        
        self.assertEqual(response, {"data": "test"})
        mock_make_request.assert_called_once()
        self.assertEqual(mock_make_request.call_args[1]["method"], RequestMethod.POST)
    
    def test_get_client_for_carrier(self):
        """Test getting the client class for a carrier."""
        self.assertEqual(get_client_for_carrier(Carrier.UPS), UPSClient)
        self.assertEqual(get_client_for_carrier(Carrier.FEDEX), FedExClient)
        self.assertEqual(get_client_for_carrier(Carrier.USPS), USPSClient)
        self.assertEqual(get_client_for_carrier(Carrier.DHL), DHLClient)
        self.assertEqual(get_client_for_carrier(Carrier.AMAZON), AmazonClient)
        
        with self.assertRaises(ValueError) as context:
            get_client_for_carrier(Carrier.UNKNOWN)
        
        self.assertIn("Unsupported carrier", str(context.exception))


if __name__ == "__main__":
    unittest.main()
