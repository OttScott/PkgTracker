# Package Tracker

This package provides simple utilities for detecting a carrier from a
tracking number and querying shipment status from various carrier APIs.

## Configuration

API credentials are read from environment variables. Set the following
variables to enable API calls:

- `UPS_API_KEY`
- `FEDEX_API_KEY`
- `USPS_API_KEY`
- `DHL_API_KEY`
- `AMAZON_API_KEY`

If a variable is unset, the corresponding request will still be sent but
without credentials which may lead to authentication failures.

