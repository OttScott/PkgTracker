import unittest
from unittest.mock import patch, Mock
from tracker.carriers import Carrier
from tracker.fetch_status import (
    fetch_status, fetch_ups_status, fetch_fedex_status,
    fetch_usps_status, fetch_dhl_status, fetch_amazon_status
)
from tracker.http_client import APIError

class TestFetchStatus(unittest.TestCase):
    @patch('tracker.fetch_status.fetch_ups_status')
    def test_mock_response_structure(self, mock_fetch_ups):
        """Test that fetch_status returns a dict with expected keys."""
        # Configure the mock to return a predefined response
        mock_fetch_ups.return_value = {
            "status": "Delivered",
            "estimated_delivery": "2025-06-05",
            "current_location": "Los Angeles, CA"
        }
        
        result = fetch_status(Carrier.UPS, "1Z12345E0291980793")
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("estimated_delivery", result)
        self.assertIn("current_location", result)
        # Verify the mock was called with the right arguments
        mock_fetch_ups.assert_called_once_with("1Z12345E0291980793")
    
    @patch('tracker.fetch_status.fetch_ups_status')
    @patch('tracker.fetch_status.fetch_fedex_status')
    @patch('tracker.fetch_status.fetch_usps_status')
    @patch('tracker.fetch_status.fetch_dhl_status')
    @patch('tracker.fetch_status.fetch_amazon_status')
    def test_fetch_status_with_all_carriers(self, mock_amazon, mock_dhl, mock_usps, mock_fedex, mock_ups):
        """Test fetch_status works with all supported carriers."""
        # Configure all mocks to return valid responses
        mock_response = {
            "status": "In Transit",
            "estimated_delivery": "2025-06-20",
            "current_location": "Test Location"
        }
        mock_ups.return_value = mock_response
        mock_fedex.return_value = mock_response
        mock_usps.return_value = mock_response
        mock_dhl.return_value = mock_response
        mock_amazon.return_value = mock_response
        
        carriers = [
            Carrier.UPS,
            Carrier.FEDEX,
            Carrier.USPS,
            Carrier.DHL,
            Carrier.AMAZON
        ]
        
        for carrier in carriers:
            with self.subTest(carrier=carrier):
                result = fetch_status(carrier, "test-tracking-number")
                self.assertIsInstance(result, dict)
                self.assertIn("status", result)
                self.assertEqual(result["status"], "In Transit")
                self.assertIn("estimated_delivery", result)
                self.assertIn("current_location", result)
    
    def test_fetch_status_unsupported_carrier(self):
        """Test fetch_status returns None for unsupported carriers."""
        with patch("builtins.print") as mock_print:
            result = fetch_status(Carrier.UNKNOWN, "test-tracking-number")
            self.assertIsNone(result)
            mock_print.assert_called_once()
            self.assertIn("Unsupported carrier", mock_print.call_args[0][0])
    
    @patch('tracker.http_client.UPSClient.get_tracking_info')
    def test_ups_response_structure(self, mock_ups_api):
        """Test UPS tracking response structure with mocked API call."""
        # Configure the mock to return a valid API response
        mock_ups_api.return_value = {
            "trackResponse": {
                "shipment": [
                    {
                        "package": [
                            {
                                "activity": [
                                    {
                                        "status": {
                                            "description": "Delivered"
                                        },
                                        "location": {
                                            "address": {
                                                "city": "Los Angeles",
                                                "stateProvince": "CA"
                                            }
                                        }
                                    }
                                ]
                            }
                        ],
                        "deliveryDate": [
                            {"year": "2025", "month": "06", "day": "05"}
                        ]
                    }
                ]
            }
        }
        
        result = fetch_ups_status("1Z12345E0291980793")
        self.assertEqual(result["status"], "Delivered")
        self.assertEqual(result["estimated_delivery"], "2025-06-05")
        self.assertEqual(result["current_location"], "Los Angeles, CA")
        
        # Verify the mock was called with the right arguments
        mock_ups_api.assert_called_once_with("1Z12345E0291980793")
    
    @patch('tracker.http_client.FedExClient.get_tracking_info')
    def test_fedex_response_structure(self, mock_fedex_api):
        """Test FedEx tracking response structure with mocked API call."""
        # Configure the mock to return a valid API response
        mock_fedex_api.return_value = {
            "output": {
                "completeTrackResults": [
                    {
                        "trackResults": [
                            {
                                "latestStatusDetail": {
                                    "description": "In Transit"
                                },
                                "deliveryDetails": {
                                    "deliveryDate": "2025-06-06"
                                },
                                "scanEvents": [
                                    {
                                        "scanLocation": {
                                            "city": "Chicago",
                                            "stateOrProvinceCode": "IL"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        
        result = fetch_fedex_status("123456789012")
        self.assertEqual(result["status"], "In Transit")
        self.assertEqual(result["estimated_delivery"], "2025-06-06")
        self.assertEqual(result["current_location"], "Chicago, IL")
        
        # Verify the mock was called with the right arguments
        mock_fedex_api.assert_called_once_with("123456789012")
    
    @patch('tracker.http_client.USPSClient.get_tracking_info')
    def test_usps_response_structure(self, mock_usps_api):
        """Test USPS tracking response structure with mocked API call."""
        # USPS returns XML which our test is simulating as already converted to a dict
        mock_usps_api.return_value = {
            "xml_response": """
                <TrackResponse>
                    <TrackInfo ID="9400110897700000000000">
                        <Status>Out for Delivery</Status>
                        <ExpectedDeliveryDate>2025-06-05</ExpectedDeliveryDate>
                        <City>New York</City>
                        <State>NY</State>
                    </TrackInfo>
                </TrackResponse>
            """
        }
        
        result = fetch_usps_status("9400110897700000000000")
        self.assertEqual(result["status"], "Out for Delivery")
        self.assertEqual(result["estimated_delivery"], "2025-06-05")
        self.assertEqual(result["current_location"], "New York, NY")
        
        # Verify the mock was called with the right arguments
        mock_usps_api.assert_called_once_with("9400110897700000000000")
    
    @patch('tracker.http_client.DHLClient.get_tracking_info')
    def test_dhl_response_structure(self, mock_dhl_api):
        """Test DHL tracking response structure with mocked API call."""
        # Configure the mock to return a valid API response
        mock_dhl_api.return_value = {
            "shipments": [
                {
                    "status": {
                        "description": "Delivered"
                    },
                    "estimatedDeliveryDate": "2025-06-04",
                    "events": [
                        {
                            "location": {
                                "address": {
                                    "city": "San Francisco",
                                    "countryCode": "CA"
                                }
                            }
                        }
                    ]
                }
            ]
        }
        
        result = fetch_dhl_status("3S1234567890")
        self.assertEqual(result["status"], "Delivered")
        self.assertEqual(result["estimated_delivery"], "2025-06-04")
        self.assertEqual(result["current_location"], "San Francisco, CA")
        
        # Verify the mock was called with the right arguments
        mock_dhl_api.assert_called_once_with("3S1234567890")
    
    @patch('tracker.http_client.AmazonClient.get_tracking_info')
    def test_amazon_response_structure(self, mock_amazon_api):
        """Test Amazon tracking response structure with mocked API call."""
        # Configure the mock to return a valid API response
        mock_amazon_api.return_value = {
            "trackingInfo": {
                "status": "Shipped",
                "estimatedDelivery": "2025-06-07",
                "currentLocation": {
                    "description": "Seattle, WA"
                }
            }
        }
        
        result = fetch_amazon_status("TBA123456789")
        self.assertEqual(result["status"], "Shipped")
        self.assertEqual(result["estimated_delivery"], "2025-06-07")
        self.assertEqual(result["current_location"], "Seattle, WA")
        
        # Verify the mock was called with the right arguments
        mock_amazon_api.assert_called_once_with("TBA123456789")

if __name__ == "__main__":
    unittest.main()
