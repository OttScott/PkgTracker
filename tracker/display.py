def display_tracking_info(data: dict) -> None:
  if (data is None or 
      not isinstance(data, dict)):
      # not all(key in data for key in ["status", "estimated_delivery", "current_location"])):
    print("Invalid tracking data provided.")
    raise ValueError("Invalid tracking data structure")
    return
  print("\nTracking Info:")
  print(f"Status: {data.get('status')}")
  print(f"Estimated Delivery: {data.get('estimated_delivery')}")
  print(f"Current Location: {data.get('current_location')}")

