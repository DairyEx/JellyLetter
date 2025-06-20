import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, NEWSLETTER_TO

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("newsletter.html.j2")

def send_newsletter(context):
    html = template.render(**context)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = context["subject"]
    msg["From"]    = SMTP_USER
    msg["To"]      = NEWSLETTER_TO
    msg.attach(MIMEText(html, "html"))

    context_ssl = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context_ssl)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
