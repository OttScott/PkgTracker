import unittest
from tracker.fetch_status import fetch_status

class TestFetchStatus(unittest.TestCase):
  def test_mock_response_structure(self):
    result = fetch_status("UPS", "1Z12345E0291980793")
    self.assertIsInstance(result, dict)
    self.assertIn("status", result)
    self.assertIn("estimated_delivery", result)
    self.assertIn("current_location", result)

if __name__ == "__main__":
  unittest.main()
