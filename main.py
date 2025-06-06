import sys
import argparse
from tracker.logging import set_log_level, LogLevel
from tracker.detect_carrier import detect_carrier
from tracker.fetch_status import fetch_status
from tracker.display import display_tracking_info

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("--debug", action="store_true", help="Enable debug logging")
  parser.add_argument("--tracking_number", type=str, required=True, help="Tracking number to fetch status for")
  args = parser.parse_args()

  if args.debug:
    set_log_level(LogLevel.DEBUG)
  else:
    set_log_level(LogLevel.INFO)
  
  print(f"Tracking number provided: {args.tracking_number}")
  carrier = detect_carrier(args.tracking_number)
  if carrier is None:
    print("Could not detect carrier.")
    sys.exit(1)

  data = fetch_status(carrier, args.tracking_number)
  if data is None:
    print("Failed to fetch tracking information.")
    sys.exit(1)

  display_tracking_info(data)

if __name__ == "__main__":
#  args = parser.parse_args()
  main()