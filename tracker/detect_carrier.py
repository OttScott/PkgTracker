import re
from tracker.carriers import Carrier
from tracker.logging import log_function_call

@log_function_call()
def detect_carrier(tracking_number: str) -> Carrier:
  tracking_number = tracking_number.lower().strip()

  # UPS: starts with 1Z
  if tracking_number.startswith("1z"):
    return Carrier.UPS

  # FedEx: often 12–14 digit numbers
  if re.fullmatch(r"\d{12,14}", tracking_number):
    return Carrier.FEDEX

  # DHL: usually starts with 3S, JJD, or similar
  if re.fullmatch(r"(3S|JJD)\d{10,20}", tracking_number):
    return Carrier.DHL
  
  # Amazon: usually starts with TBA
  if tracking_number.startswith("TBA"):
    return Carrier.AMAZON
  
  # USPS: usually 20-22 digits, often start with 94
  if re.fullmatch(r"\d{20,22}", tracking_number) and tracking_number.startswith("94"):
    return Carrier.USPS

  return Carrier.UNKNOWN
