import os

JELLYFIN_URL   = os.getenv("JELLYFIN_URL", "http://jellyfin:8096")
API_KEY        = os.getenv("JELLYFIN_API_KEY")
SMTP_SERVER    = os.getenv("SMTP_SERVER")
SMTP_PORT      = int(os.getenv("SMTP_PORT", 587))
SMTP_USER      = os.getenv("SMTP_USER")
SMTP_PASS      = os.getenv("SMTP_PASS")
NEWSLETTER_TO  = os.getenv("NEWSLETTER_TO")
