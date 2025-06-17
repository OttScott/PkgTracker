from enum import Enum

class Carrier(Enum):
  UPS = "UPS"
  FEDEX = "FedEx"
  USPS = "USPS"
  DHL = "DHL"
  AMAZON = "Amazon"
  UNKNOWN = "Unknown"