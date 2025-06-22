"""
Tests for the carriers module.
"""
import unittest
from tracker.carriers import Carrier

class TestCarriers(unittest.TestCase):
    def test_carrier_enum_values(self):
        """Test that Carrier enum has the expected values."""
        self.assertEqual(Carrier.UPS.value, "UPS")
        self.assertEqual(Carrier.FEDEX.value, "FedEx")
        self.assertEqual(Carrier.USPS.value, "USPS")
        self.assertEqual(Carrier.DHL.value, "DHL")
        self.assertEqual(Carrier.AMAZON.value, "Amazon")
        self.assertEqual(Carrier.UNKNOWN.value, "Unknown")
    
    def test_carrier_enum_count(self):
        """Test the number of carriers in the enum."""
        self.assertEqual(len(Carrier), 6)
    
    def test_carrier_enum_membership(self):
        """Test checking if a value is in the Carrier enum."""
        self.assertIn(Carrier.UPS, Carrier)
        self.assertIn(Carrier.FEDEX, Carrier)
        self.assertIn(Carrier.USPS, Carrier)
        self.assertIn(Carrier.DHL, Carrier)
        self.assertIn(Carrier.AMAZON, Carrier)
        self.assertIn(Carrier.UNKNOWN, Carrier)
    
    def test_carrier_string_representation(self):
        """Test string representation of Carrier enum values."""
        self.assertEqual(str(Carrier.UPS), "Carrier.UPS")
        self.assertEqual(str(Carrier.FEDEX), "Carrier.FEDEX")
        self.assertEqual(str(Carrier.USPS), "Carrier.USPS")
        self.assertEqual(str(Carrier.DHL), "Carrier.DHL")
        self.assertEqual(str(Carrier.AMAZON), "Carrier.AMAZON")
        self.assertEqual(str(Carrier.UNKNOWN), "Carrier.UNKNOWN")

if __name__ == "__main__":
    unittest.main()
