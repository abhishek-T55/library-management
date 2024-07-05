from celery import Celery

celery_app = Celery(
    __name__,
    broker="redis://default:password@localhost:6379/0",
    backend="redis://default:password@localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


