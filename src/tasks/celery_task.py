import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import settings, BASE_DIR

celery = Celery('tasks', broker=settings.RABBIT_URL)
celery.conf.broker_connection_retry_on_startup = True
celery.conf.result_backend = 'rpc://'


@celery.task
def send_email_to_dealer(dealer_email: str, file_name: str):
    email = EmailMessage()
    email['Subject'] = 'Accept Order'
    email['From'] = settings.SMTP_USER
    email['To'] = dealer_email
    email.set_content('Where is the money, Lebovski?')

    file_path = f'{BASE_DIR}/documents/{file_name}'

    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_name = file.name

    email.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
