import logging
import requests
from config import JELLYFIN_URL, API_KEY

HEADERS = {"X-Emby-Token": API_KEY}


def _get_json(url: str, **kwargs) -> dict:
    """Perform a GET request and parse the JSON response.

    Any network issues or JSON decoding errors are caught and an empty
    dictionary is returned instead so the rest of the app can continue
    to operate without crashing.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # pragma: no cover - simple error log
        logging.warning("Failed to fetch %s: %s", url, exc)
        return {}

def get_recently_added(days: int = 7):
    """Return recently added items or an empty list on failure."""
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
    data = _get_json(f"{JELLYFIN_URL}/Reports/MostPlayedItems")
    if isinstance(data, list):
        return data[:top_n]
    return []
