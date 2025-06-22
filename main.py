#!/usr/bin/env python3
"""
Package Tracker CLI
A command-line tool to track packages across multiple carriers.
"""

import sys
import argparse
from tracker.carriers import Carrier
from tracker.detect_carrier import detect_carrier
from tracker.fetch_status import fetch_status
from tracker.display import display_tracking_info
from tracker.http_client import APIError

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Track packages across multiple carriers."
    )
    parser.add_argument(
        "tracking_number", 
        help="Tracking number to fetch status for"
    )
    parser.add_argument(
        "--carrier", "-c",
        type=str,
        choices=[c.value for c in Carrier],
        help="Specify the carrier (optional, will auto-detect if not provided)"
    )
    parser.add_argument(
        "--version", "-v", 
        action="version", 
        version="Package Tracker CLI v1.0.0"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the package tracker CLI."""
    try:
        args = parse_arguments()
        
        print(f"Tracking number: {args.tracking_number}")
        
        # Detect or use specified carrier
        if args.carrier:
            try:
                carrier = Carrier(args.carrier)
                print(f"Using specified carrier: {carrier.value}")
            except ValueError:
                print(f"Error: Invalid carrier '{args.carrier}'")
                sys.exit(1)
        else:
            carrier = detect_carrier(args.tracking_number)
            if carrier == Carrier.UNKNOWN:
                print("Warning: Could not detect carrier.")
            else:
                print(f"Detected carrier: {carrier.value}")
        
        # Fetch tracking information
        print("Fetching tracking information...")
        data = fetch_status(carrier, args.tracking_number)
        if data is None:
            print("Error: Failed to fetch tracking information.")
            sys.exit(1)
        
        # Display tracking information
        display_tracking_info(data)
        
    except APIError as e:
        print(f"API Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()