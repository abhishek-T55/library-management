from celery_worker import celery_app
from app.services.email import DummyEmailService

@celery_app.task
def send_registration_email(email: str):
    DummyEmailService.send_registration_email(email)