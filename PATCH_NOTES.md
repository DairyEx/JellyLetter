# Patch Notes

## Issue
- Unhandled network failures to the Jellyfin server caused the Flask app to crash when dashboard endpoints attempted to fetch recent activity.
- Logs showed `socket.gaierror: [Errno -2] Name or service not known` raised from `urllib3` inside a request to Jellyfin.

## Fix
- Wrapped Jellyfin API requests in a new helper `_get_json` that handles `requests.RequestException` and JSON decoding errors.
- Failed requests now log a warning and return an empty structure so pages render gracefully.
- Added small improvements from review comments: explicit typing for the helper and separate handling for malformed JSON responses.

## Issue
- Warnings showed `NameResolutionError` when requesting `http://your-jellyfin:8096`, meaning the example `JELLYFIN_URL` was left unchanged.

## Fix
- Documented that the `JELLYFIN_URL` environment variable must point to your real server.
- Updated `docker-compose.yml` to default to `http://jellyfin:8096` and added a comment as a reminder.

## Issue
- Using `http://jellyfin:8096` as the default Jellyfin URL still caused errors if no server was reachable.

## Fix
- Removed the default URL so `JELLYFIN_URL` starts empty and is configured via the Settings page.
- Updated `docker-compose.yml`, `config.example.json`, and the README accordingly.
- `jellyfin_client` now warns and returns empty data when the URL isn't set.
