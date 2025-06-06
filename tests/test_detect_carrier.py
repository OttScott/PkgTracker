import unittest
from tracker.carriers import Carrier
from tracker.detect_carrier import detect_carrier

class TestDetectCarrier(unittest.TestCase):
  def test_ups_tracking(self):
    self.assertEqual(detect_carrier("1Z12345E0291980793"), Carrier.UPS)

  def test_fedex_tracking(self):
    self.assertEqual(detect_carrier("61299998765432"), Carrier.FEDEX)  # Placeholder

  def test_usps_tracking(self):
    self.assertEqual(detect_carrier("9400110897700000000000"), Carrier.USPS)  # Placeholder

  def test_invalid_tracking(self):
    self.assertEqual(detect_carrier(Carrier.UNKNOWN.value), Carrier.UNKNOWN)  # Placeholder for invalid tracking number


if __name__ == "__main__":
  unittest.main()
