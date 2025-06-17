from enum import Enum
from tracker.carriers import Carrier
from tracker.logging import log_function_call
from tracker.http_client import get_oauth_token
import requests

@log_function_call()
def fetch_status(carrier: Carrier, tracking_number: str) -> dict | None:
    if carrier == Carrier.UPS:
        return fetch_ups_status(tracking_number)
    if carrier == Carrier.FEDEX:
        return fetch_fedex_status(tracking_number)
    if carrier == Carrier.USPS:
        return fetch_usps_status(tracking_number)
    if carrier == Carrier.DHL:
        return fetch_dhl_status(tracking_number)
    if carrier == Carrier.AMAZON:
        return fetch_amazon_status(tracking_number)
    log(f"Unsupported carrier: {carrier}", LogLevel.ERROR)
    return None


def _parse_response(data: dict) -> dict | None:
    if not isinstance(data, dict):
        return None
    return {
        "status": data.get("status"),
        "estimated_delivery": data.get("estimated_delivery"),
        "current_location": data.get("current_location"),
    }


@log_function_call()
def fetch_ups_status(tracking_number: str) -> dict:
    """Fetch tracking information from UPS using OAuth."""
    print(f"[DEBUG] Fetching status for UPS tracking #: {tracking_number}")
    token = get_oauth_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://wwwcie.ups.com/track/v1/details/{tracking_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


@log_function_call()
def fetch_fedex_status(tracking_number: str) -> dict | None:
    url = f"https://api.fedex.com/track/v1/{tracking_number}"
    params = {"token": os.getenv("FEDEX_API_KEY")}
    data = get_json(url, params=params)
    return _parse_response(data)


@log_function_call()
def fetch_usps_status(tracking_number: str) -> dict | None:
    url = f"https://api.usps.com/track/v1/{tracking_number}"
    params = {"api_key": os.getenv("USPS_API_KEY")}
    data = get_json(url, params=params)
    return _parse_response(data)


@log_function_call()
def fetch_dhl_status(tracking_number: str) -> dict | None:
    url = f"https://api.dhl.com/track/shipments/{tracking_number}"
    params = {"api_key": os.getenv("DHL_API_KEY")}
    data = get_json(url, params=params)
    return _parse_response(data)


@log_function_call()
def fetch_amazon_status(tracking_number: str) -> dict | None:
    url = f"https://api.amazon.com/track/v1/packages/{tracking_number}"
    params = {"access_token": os.getenv("AMAZON_API_KEY")}
    data = get_json(url, params=params)
    return _parse_response(data)
