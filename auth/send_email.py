import smtplib
from email.message import EmailMessage

from config import SMTP_USER, SMTP_PASS


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template(username: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Some_store verify'
    email['From'] = SMTP_USER
    email['To'] = username

    email.set_content(
        '<div>'
        f'<h1>Здравствуйте, {username}, вот ваш токен:</h1>'
        f'<h2>{token}</h2>'
        '</div>',
        subtype='html'
    )
    return email


def send_email(username: str, token: str):
    email = get_email_template(username, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)

