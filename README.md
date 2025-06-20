# JellyLetter Newsletter Service

A Dockerized Python service for generating and sending email newsletters based on Jellyfin server usage statistics.

## Features

- Fetches recently added and most-watched items via Jellyfin API
- Renders HTML newsletters using Jinja2
- Sends emails via SMTP
- Web-based GUI with Flask for stats overview and settings
- APScheduler for configurable scheduling

## Usage

1. Configure environment variables in `docker-compose.yml` or your environment.
2. Build and run:
   ```bash
   docker-compose up --build -d
   ```
3. Access GUI at `http://<host>:5000`
4. Configure settings and schedule, or click "Send Now" to trigger a newsletter immediately.
