import unittest
from tracker.carriers import Carrier
from tracker.detect_carrier import detect_carrier

class TestDetectCarrier(unittest.TestCase):
    def test_ups_tracking(self):
        """Test UPS tracking number detection."""
        # Standard UPS format
        self.assertEqual(detect_carrier("1Z12345E0291980793"), Carrier.UPS)
        # Lowercase
        self.assertEqual(detect_carrier("1z12345e0291980793"), Carrier.UPS)
        # With spaces
        self.assertEqual(detect_carrier(" 1Z12345E0291980793 "), Carrier.UPS)
    
    def test_fedex_tracking(self):
        """Test FedEx tracking number detection."""
        # 12 digits
        self.assertEqual(detect_carrier("612999987654"), Carrier.FEDEX)
        # 14 digits
        self.assertEqual(detect_carrier("61299998765432"), Carrier.FEDEX)
        # With spaces
        self.assertEqual(detect_carrier(" 61299998765432 "), Carrier.FEDEX)
    
    def test_usps_tracking(self):
        """Test USPS tracking number detection."""
        # 20 digits starting with 94
        self.assertEqual(detect_carrier("94001108977000000000"), Carrier.USPS)
        # 22 digits starting with 94
        self.assertEqual(detect_carrier("9400110897700000000000"), Carrier.USPS)
        # With spaces
        self.assertEqual(detect_carrier(" 9400110897700000000000 "), Carrier.USPS)
    
    def test_dhl_tracking(self):
        """Test DHL tracking number detection."""
        # Starting with 3S
        self.assertEqual(detect_carrier("3S1234567890123"), Carrier.DHL)
        # Starting with JJD
        self.assertEqual(detect_carrier("JJD1234567890123"), Carrier.DHL)
        # With spaces
        self.assertEqual(detect_carrier(" JJD1234567890123 "), Carrier.DHL)
    
    def test_amazon_tracking(self):
        """Test Amazon tracking number detection."""
        # Standard TBA format
        self.assertEqual(detect_carrier("TBA123456789"), Carrier.AMAZON)
        # Lowercase
        self.assertEqual(detect_carrier("tba123456789"), Carrier.AMAZON)
        # With spaces
        self.assertEqual(detect_carrier(" TBA123456789 "), Carrier.AMAZON)
    
    def test_invalid_tracking(self):
        """Test invalid tracking numbers."""
        # Empty string
        self.assertEqual(detect_carrier(""), Carrier.UNKNOWN)
        # Random string
        self.assertEqual(detect_carrier("not-a-tracking-number"), Carrier.UNKNOWN)
        # Number only
        self.assertEqual(detect_carrier("12345"), Carrier.UNKNOWN)
        # Using carrier value directly
        self.assertEqual(detect_carrier(Carrier.UNKNOWN.value), Carrier.UNKNOWN)
    
    def test_edge_cases(self):
        """Test edge cases in tracking number detection."""
        # Long numeric string not matching any pattern
        self.assertEqual(detect_carrier("12345678901234567890"), Carrier.UNKNOWN)
        # Almost UPS but wrong prefix
        self.assertEqual(detect_carrier("2Z12345E0291980793"), Carrier.UNKNOWN)

if __name__ == "__main__":
    unittest.main()
