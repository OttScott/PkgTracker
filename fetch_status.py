from enum import Enum
from tracker.carriers import Carrier
from tracker.logging import log_function_call

@log_function_call()
def fetch_status(carrier: Carrier, tracking_number: str) -> dict | None:
  match (carrier):
    case Carrier.UPS:
      return fetch_ups_status(tracking_number)
    case Carrier.FEDEX:
      return fetch_fedex_status(tracking_number)
    case Carrier.USPS:
      return fetch_usps_status(tracking_number)
    case Carrier.DHL:
      return fetch_dhl_status(tracking_number)
    case Carrier.AMAZON:
      return fetch_amazon_status(tracking_number)
    case _:
      print(f"[ERROR] Unsupported carrier: {carrier}")
      return None   

@log_function_call()
def fetch_ups_status(tracking_number: str) -> dict:
  # Simulated API call to UPS tracking service
  print(f"[DEBUG] Fetching status for UPS tracking #: {tracking_number}")
 
  return {
    "status": "Delivered",
    "estimated_delivery": "2025-06-05",
    "current_location": "Los Angeles, CA"
  }
  
@log_function_call()
def fetch_fedex_status(tracking_number: str) -> dict:
  # Simulated API call to FedEx tracking service
  print(f"[DEBUG] Fetching status for FedEx tracking #: {tracking_number}")
  return {
    "status": "In Transit",
    "estimated_delivery": "2025-06-06",
    "current_location": "Chicago, IL"
  }

@log_function_call()
def fetch_usps_status(tracking_number: str) -> dict:
  # Simulated API call to USPS tracking service
  print(f"[DEBUG] Fetching status for USPS tracking #: {tracking_number}")
  return {
    "status": "Out for Delivery",
    "estimated_delivery": "2025-06-05",
    "current_location": "New York, NY"
  }

@log_function_call()
def fetch_dhl_status(tracking_number: str) -> dict:
  # Simulated API call to DHL tracking service
  print(f"[DEBUG] Fetching status for DHL tracking #: {tracking_number}")
  return {
    "status": "Delivered",
    "estimated_delivery": "2025-06-04",
    "current_location": "San Francisco, CA"
  }

@log_function_call()
def fetch_amazon_status(tracking_number: str) -> dict:
  # Simulated API call to Amazon tracking service
  print(f"[DEBUG] Fetching status for Amazon tracking #: {tracking_number}")
  return {
    "status": "Shipped",
    "estimated_delivery": "2025-06-07",
    "current_location": "Seattle, WA"
  }

# Note: In a real implementation, these functions would make HTTP requests to the respective carrier's API
# and handle any errors or exceptions that may occur.
