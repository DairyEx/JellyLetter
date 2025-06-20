import requests
from config import JELLYFIN_URL, API_KEY

HEADERS = {"X-Emby-Token": API_KEY}

def get_recently_added(days=7):
    params = {"Recursive": True, "Limit": 20, "SortBy": "DateCreated", "SortOrder": "Descending"}
    resp = requests.get(f"{JELLYFIN_URL}/Items/Latest", headers=HEADERS, params=params)
    return resp.json().get("Items", [])

def get_most_watched(top_n=5):
    resp = requests.get(f"{JELLYFIN_URL}/Reports/MostPlayedItems", headers=HEADERS)
    return resp.json()[:top_n]
