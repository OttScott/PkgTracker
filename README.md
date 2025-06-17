# Package Tracker

Sample tracking utility.

## UPS OAuth Configuration

The UPS tracking client requires OAuth credentials. Set the following
environment variables before running the application or tests:

- `UPS_CLIENT_ID` – UPS client identifier used to request a token.
- `UPS_CLIENT_SECRET` – UPS client secret used to request a token.

A valid token will be automatically requested and cached until it expires.
