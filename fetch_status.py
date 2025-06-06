def fetch_status(carrier: str, tracking_number: str) -> dict | None:
  # TODO: Call real API later
  print(f"[DEBUG] Fetching status for {carrier} tracking #: {tracking_number}")
  return {
    "status": "In Transit",
    "estimated_delivery": "2025-06-07",
    "current_location": "Memphis, TN"
  }
