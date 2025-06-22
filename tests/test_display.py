import unittest
from unittest.mock import patch, call
from tracker.display import display_tracking_info

class TestDisplay(unittest.TestCase):
    @patch("builtins.print")
    def test_output_structure(self, mock_print):
        """Test that display_tracking_info outputs the correct structure with valid data."""
        display_tracking_info({
            "carrier": "UPS", 
            "tracking_number": "1Z999AA10123456784",
            "status": "In Transit",
            "estimated_delivery": "2023-10-15",
            "current_location": "New York, NY"
        })
        calls = [call_arg[0][0] for call_arg in mock_print.call_args_list]
        
        # Check header is displayed
        self.assertTrue(any("Tracking Info:" in call for call in calls))
        
        # Check all tracking fields are displayed
        self.assertTrue(any("Status: In Transit" in call for call in calls))
        self.assertTrue(any("Estimated Delivery: 2023-10-15" in call for call in calls))
        self.assertTrue(any("Current Location: New York, NY" in call for call in calls))
        
        # Check the order of output
        self.assertEqual(mock_print.call_args_list[0], call("\nTracking Info:"))
        self.assertEqual(mock_print.call_args_list[1], call("Status: In Transit"))
        self.assertEqual(mock_print.call_args_list[2], call("Estimated Delivery: 2023-10-15"))
        self.assertEqual(mock_print.call_args_list[3], call("Current Location: New York, NY"))
    
    @patch("builtins.print")
    def test_missing_fields(self, mock_print):
        """Test handling of missing fields in the tracking data."""
        display_tracking_info({
            "carrier": "FEDEX",
            "tracking_number": "123456789012"
            # Missing status, estimated_delivery, and current_location
        })
        
        # Check that None is displayed for missing fields
        self.assertEqual(mock_print.call_args_list[1], call("Status: None"))
        self.assertEqual(mock_print.call_args_list[2], call("Estimated Delivery: None"))
        self.assertEqual(mock_print.call_args_list[3], call("Current Location: None"))
    
    @patch("builtins.print")
    def test_none_data(self, mock_print):
        """Test handling of None data."""
        with self.assertRaises(ValueError) as context:
            display_tracking_info(None)
        
        self.assertEqual(str(context.exception), "Invalid tracking data structure")
        mock_print.assert_called_once_with("Invalid tracking data provided.")
    
    @patch("builtins.print")
    def test_non_dict_data(self, mock_print):
        """Test handling of non-dictionary data."""
        with self.assertRaises(ValueError) as context:
            display_tracking_info("not_a_dict")
        
        self.assertEqual(str(context.exception), "Invalid tracking data structure")
        mock_print.assert_called_once_with("Invalid tracking data provided.")
    
    @patch("builtins.print")
    def test_empty_dict(self, mock_print):
        """Test handling of an empty dictionary."""
        display_tracking_info({})
        
        self.assertEqual(mock_print.call_args_list[1], call("Status: None"))
        self.assertEqual(mock_print.call_args_list[2], call("Estimated Delivery: None"))
        self.assertEqual(mock_print.call_args_list[3], call("Current Location: None"))

if __name__ == "__main__":
    unittest.main()
