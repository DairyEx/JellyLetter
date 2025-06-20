import logging
from typing import Any, Dict

import requests
from config import JELLYFIN_URL, API_KEY

HEADERS = {"X-Emby-Token": API_KEY}


def _get_json(url: str, **kwargs) -> Dict[str, Any] | list:
    """Return JSON from ``url`` or an empty structure on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as exc:  # pragma: no cover - network errors
        logging.warning("Failed to fetch %s: %s", url, exc)
    except ValueError as exc:  # pragma: no cover - JSON decode error
        logging.warning("Invalid JSON from %s: %s", url, exc)
    return {}

def get_recently_added(days: int = 7):
    """Return recently added items or an empty list on failure."""
    if not JELLYFIN_URL:
        logging.warning("JELLYFIN_URL not configured")
        return []
    params = {
        "Recursive": True,
        "Limit": 20,
        "SortBy": "DateCreated",
        "SortOrder": "Descending",
    }
    data = _get_json(f"{JELLYFIN_URL}/Items/Latest", params=params)
    return data.get("Items", [])

def get_most_watched(top_n: int = 5):
    """Return the most watched items or an empty list on failure."""
    if not JELLYFIN_URL:
        logging.warning("JELLYFIN_URL not configured")
        return []
    data = _get_json(f"{JELLYFIN_URL}/Reports/MostPlayedItems")
    if isinstance(data, list):
        return data[:top_n]
    return []
