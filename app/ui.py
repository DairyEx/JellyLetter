from flask import Blueprint, render_template, request, redirect, url_for, flash
import config
from jellyfin_client import get_recently_added, get_most_watched
from newsletter import send_newsletter

ui = Blueprint("ui", __name__, template_folder="templates", static_folder="static")

@ui.route("/")
def dashboard():
    new_items = get_recently_added()
    top_watched = get_most_watched()
    return render_template("dashboard.html", new_items=new_items, top_watched=top_watched)


@ui.route("/stats")
def stats():
    from pathlib import Path
    log_file = Path(__file__).resolve().parent / "logs" / "newsletter.log"
    entries = []
    if log_file.exists():
        with open(log_file) as fh:
            entries = fh.readlines()[-50:][::-1]  # newest first
    return render_template("stats.html", log_entries=entries)

@ui.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        config.JELLYFIN_URL = request.form.get("jellyfin_url")
        config.API_KEY = request.form.get("api_key")
        config.SMTP_SERVER = request.form.get("smtp_server")
        config.SMTP_PORT = int(request.form.get("smtp_port", 587))
        config.SMTP_USER = request.form.get("smtp_user")
        config.SMTP_PASS = request.form.get("smtp_pass")
        config.NEWSLETTER_TO = request.form.get("newsletter_to")
        config.DISCORD_WEBHOOK_URL = request.form.get("discord_webhook_url")
        config.TELEGRAM_BOT_TOKEN = request.form.get("telegram_bot_token")
        config.TELEGRAM_CHAT_ID = request.form.get("telegram_chat_id")
        config.save()
        flash("Settings saved!", "success")
        return redirect(url_for("ui.settings"))
    return render_template(
        "settings.html",
        jellyfin_url=config.JELLYFIN_URL,
        api_key=config.API_KEY,
        smtp_server=config.SMTP_SERVER,
        smtp_port=config.SMTP_PORT,
        smtp_user=config.SMTP_USER,
        smtp_pass=config.SMTP_PASS,
        newsletter_to=config.NEWSLETTER_TO,
        discord_webhook_url=config.DISCORD_WEBHOOK_URL,
        telegram_bot_token=config.TELEGRAM_BOT_TOKEN,
        telegram_chat_id=config.TELEGRAM_CHAT_ID,
    )

@ui.route("/send-now")
def send_now():
    from datetime import datetime
    ctx = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "new_items": get_recently_added(),
        "top_watched": get_most_watched(),
        "subject": f"Your Jellyfin Summary — {datetime.now():%B %d, %Y}"
    }
    send_newsletter(ctx)
    flash("Newsletter sent!", "info")
    return redirect(url_for("ui.dashboard"))
