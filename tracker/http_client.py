import os
import time
import requests
from __future__ import annotations
from typing import Any, Dict, Optional
import requests
from requests import RequestException
from .logging import log, LogLevel

_token_cache = {"token": None, "expires_at": 0.0}

def get_oauth_token() -> str:
    """Retrieve and cache UPS OAuth token."""
    if _token_cache["token"] and _token_cache["expires_at"] > time.time():
        return _token_cache["token"]

    client_id = os.environ.get("UPS_CLIENT_ID")
    client_secret = os.environ.get("UPS_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise EnvironmentError("UPS_CLIENT_ID and UPS_CLIENT_SECRET must be set")

    url = "https://wwwcie.ups.com/security/v1/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    data = response.json()

    token = data["access_token"]
    expires_in = int(data.get("expires_in", 3600))
    _token_cache["token"] = token
    _token_cache["expires_at"] = time.time() + expires_in - 10
    return token

def get_json(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> Optional[Dict[str, Any]]:
    """Fetch JSON data from a URL with basic error handling."""
    try:
        log(f"GET {url} params={params}", LogLevel.DEBUG)
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        log(f"Received {response.status_code} from {url}", LogLevel.DEBUG)
        return response.json()
    except RequestException as exc:
        log(f"HTTP request failed: {exc}", LogLevel.ERROR)
    except ValueError as exc:
        log(f"Failed to decode JSON: {exc}", LogLevel.ERROR)
    return None
