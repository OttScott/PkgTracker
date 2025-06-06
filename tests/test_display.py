import unittest
from unittest.mock import patch
from tracker.display import display_tracking_info

class TestDisplay(unittest.TestCase):
  @patch("builtins.print")
  def test_output_structure(self, mock_print):
    display_tracking_info({"carrier": "UPS", 
                           "tracking_number": "1Z999AA10123456784",
                           "status": "In Transit",
                           "estimated_delivery": "2023-10-15",
                           "current_location": "New York, NY"})
    calls = [call_arg[0][0] for call_arg in mock_print.call_args_list]
    assert any("Tracking Info:" in call for call in calls)

if __name__ == "__main__":
  unittest.main()
