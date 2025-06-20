import os
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "config.json"

def _load_defaults():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as fh:
                return json.load(fh)
        except Exception:
            return {}
    return {}

_defaults = _load_defaults()

# Jellyfin URL should be configured via the web UI. Do not assume a default.
JELLYFIN_URL = os.getenv("JELLYFIN_URL", _defaults.get("JELLYFIN_URL", ""))
API_KEY = os.getenv("JELLYFIN_API_KEY", _defaults.get("API_KEY"))
SMTP_SERVER = os.getenv("SMTP_SERVER", _defaults.get("SMTP_SERVER"))
SMTP_PORT = int(os.getenv("SMTP_PORT", _defaults.get("SMTP_PORT", 587)))
SMTP_USER = os.getenv("SMTP_USER", _defaults.get("SMTP_USER"))
SMTP_PASS = os.getenv("SMTP_PASS", _defaults.get("SMTP_PASS"))
NEWSLETTER_TO = os.getenv("NEWSLETTER_TO", _defaults.get("NEWSLETTER_TO"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", _defaults.get("DISCORD_WEBHOOK_URL"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", _defaults.get("TELEGRAM_BOT_TOKEN"))
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", _defaults.get("TELEGRAM_CHAT_ID"))


def save() -> None:
    CONFIG_FILE.write_text(
        json.dumps(
            {
                "JELLYFIN_URL": JELLYFIN_URL,
                "API_KEY": API_KEY,
                "SMTP_SERVER": SMTP_SERVER,
                "SMTP_PORT": SMTP_PORT,
                "SMTP_USER": SMTP_USER,
                "SMTP_PASS": SMTP_PASS,
                "NEWSLETTER_TO": NEWSLETTER_TO,
                "DISCORD_WEBHOOK_URL": DISCORD_WEBHOOK_URL,
                "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
                "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
            },
            indent=2,
        )
    )
