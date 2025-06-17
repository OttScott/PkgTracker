from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from requests import RequestException

from .logging import log, LogLevel


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

