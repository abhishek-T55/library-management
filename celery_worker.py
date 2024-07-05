from celery import Celery
from app.core.config import config

celery_app = Celery(
    __name__,
    broker=config.rabbitmq.url,
    backend="rpc://"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


