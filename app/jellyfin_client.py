import logging
from typing import Any, Dict, List, Union

import requests
from config import JELLYFIN_URL, API_KEY

HEADERS = {"X-Emby-Token": API_KEY}


def _url_configured() -> bool:
    """Return True if JELLYFIN_URL is set to a real address."""
    if not JELLYFIN_URL or "your-jellyfin" in JELLYFIN_URL:
        logging.warning("JELLYFIN_URL not configured; set it in Settings")
        return False
    return True


def _get_json(url: str, **kwargs) -> Union[Dict[str, Any], List[Any]]:
    """Perform a GET request and parse the JSON response.

    Any network issues or JSON decoding errors are caught and an empty
    structure is returned instead so the rest of the app can continue
    to operate without crashing.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:  # network errors
        logging.warning("Failed to fetch %s: %s", url, exc)
    except ValueError as exc:  # JSON decode error
        logging.warning("Invalid JSON from %s: %s", url, exc)
    return {}


def get_recently_added(days: int = 7) -> List[Any]:
    """Return recently added items or an empty list on failure."""
    if not _url_configured():
        return []
    params = {
        "Recursive": True,
        "Limit": 20,
        "SortBy": "DateCreated",
        "SortOrder": "Descending",
    }
    data = _get_json(f"{JELLYFIN_URL}/Items/Latest", params=params)
    if isinstance(data, dict):
        return data.get("Items", [])
    return []


def get_most_watched(top_n: int = 5) -> List[Any]:
    """Return the most watched items or an empty list on failure."""
    if not _url_configured():
        return []
    data = _get_json(f"{JELLYFIN_URL}/Reports/MostPlayedItems")
    if isinstance(data, list):
        return data[:top_n]
    return []
