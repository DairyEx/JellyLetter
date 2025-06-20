from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ui import ui
from jellyfin_client import get_recently_added, get_most_watched
from newsletter import send_newsletter
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_to_something_secret!"
app.register_blueprint(ui)

def scheduled_job():
    ctx = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "new_items": get_recently_added(),
        "top_watched": get_most_watched(),
        "subject": f"Jellyfin Summary — {datetime.now():%B %d, %Y}"
    }
    send_newsletter(ctx)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, "cron", day_of_week="mon", hour=8, minute=0)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000)
