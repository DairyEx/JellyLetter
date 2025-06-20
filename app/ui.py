from flask import Blueprint, render_template, request, redirect, url_for, flash
from config import API_KEY, JELLYFIN_URL
from jellyfin_client import get_recently_added, get_most_watched
from newsletter import send_newsletter

ui = Blueprint("ui", __name__, template_folder="templates", static_folder="static")

@ui.route("/")
def dashboard():
    new_items = get_recently_added()
    top_watched = get_most_watched()
    return render_template("dashboard.html", new_items=new_items, top_watched=top_watched)

@ui.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        # Persist settings logic here
        flash("Settings saved!", "success")
        return redirect(url_for("ui.settings"))
    return render_template("settings.html", jellyfin_url=JELLYFIN_URL, api_key=API_KEY)

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
