# Package Tracker

Sample tracking utility.

This package provides simple utilities for detecting a carrier from a
tracking number and querying shipment status from various carrier APIs.

## Configuration

API credentials are read from environment variables. Set the following
variables to enable API calls:

- `FEDEX_API_KEY`
- `USPS_API_KEY`
- `DHL_API_KEY`
- `AMAZON_API_KEY`

If a variable is unset, the corresponding request will still be sent but
without credentials which may lead to authentication failures.

## UPS OAuth Configuration

The UPS tracking client requires OAuth credentials. Set the following
environment variables before running the application or tests:

- `UPS_CLIENT_ID` – UPS client identifier used to request a token.
- `UPS_CLIENT_SECRET` – UPS client secret used to request a token.

A valid token will be automatically requested and cached until it expires.


