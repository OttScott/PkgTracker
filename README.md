# Smart Package Tracker CLI

A simple command-line tool to track packages from major carriers using just the tracking number. Automatically detects the carrier and retrieves tracking updates.

## Features

- Auto-detect carrier from tracking number
- Display estimated delivery date
- Show current location and delivery status
- Clean CLI output
- Real-time API integration with carriers (UPS, FedEx, USPS, etc.)

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API credentials:
   - Copy `.env.example` to `.env`
   - Fill in your API keys for the various carriers

   ```bash
   cp .env.example .env
   # Edit .env file with your API credentials
   ```

## API Usage

You can use the package tracker in your own Python scripts:

```python
from tracker.carriers import Carrier
from tracker.detect_carrier import detect_carrier
from tracker.fetch_status import fetch_status
from tracker.display import display_tracking_info

# Example tracking number
tracking_number = "1Z999AA10123456784"

# Auto-detect the carrier
carrier = detect_carrier(tracking_number)
print(f"Detected carrier: {carrier.value}")

# Fetch the package tracking status
tracking_info = fetch_status(carrier, tracking_number)

# Display the tracking information
display_tracking_info(tracking_info)
```

### Obtaining API Credentials

#### UPS API
1. Register for a UPS Developer Account at [UPS Developer Portal](https://www.ups.com/upsdeveloperkit)
2. Create a new app and subscribe to the Tracking API
3. Copy your Client ID, Client Secret, and API Key to your `.env` file

## Usage
```bash
python main.py 1Z999AA10123456784
