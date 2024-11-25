from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'ServiceHub_noreply@email.com'
SENDER_PASSWORD = ''

def send_message(to, subject, content_body):
    """
    Send a plain text email.

    :param to: Recipient's email address
    :param subject: Subject of the email
    :param content_body: Body content of the email
    """
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'plain'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

def send_report(to, subject, content_body):
    """
    Send an HTML email report.

    :param to: Recipient's email address
    :param subject: Subject of the email
    :param content_body: Body content of the email in HTML format
    """
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()