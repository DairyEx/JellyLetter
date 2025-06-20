# JellyLetter Newsletter Service
![Jellyletter Icon](app/static/jellyletter.png)
A Dockerized Python service for generating and sending email newsletters based on Jellyfin server usage statistics.

## Features

- Fetches recently added and most-watched items via Jellyfin API
- Renders HTML newsletters using Jinja2
- Sends emails via SMTP
- Web-based GUI with Flask for stats overview and settings
- APScheduler for configurable scheduling
- Supports ProtonMail 3rd-party SMTP tokens
- Optional Discord and Telegram notifications when a newsletter is sent

## Usage

1. Configure environment variables in `docker-compose.yml` or your environment.
2. Build and run:
   ```bash
   docker-compose up --build -d
   ```
3. Access GUI at `http://<host>:5000`
4. Configure settings and schedule, or click "Send Now" to trigger a newsletter immediately.
5. View recent send history under **Stats**.
   Settings are saved to `app/config.json` for persistence (a template is
   provided as `app/config.example.json`).

### Running Locally

If you want to launch the Flask server outside of Docker, install the Python dependencies first:

```bash
pip install -r app/requirements.txt
python app/main.py
```

### Environment Variables

```
JELLYFIN_URL          Jellyfin server URL
JELLYFIN_API_KEY      API key for Jellyfin
SMTP_SERVER           SMTP server address (works with ProtonMail tokens)
SMTP_PORT             SMTP port (e.g. 587)
SMTP_USER             SMTP username
SMTP_PASS             SMTP password or ProtonMail token
NEWSLETTER_TO         Recipient email address
DISCORD_WEBHOOK_URL   Optional Discord webhook for notifications
TELEGRAM_BOT_TOKEN    Optional Telegram bot token
TELEGRAM_CHAT_ID      Optional Telegram chat ID
```
