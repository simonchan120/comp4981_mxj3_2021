from celery import Celery
from backend import app

celery_app = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
celery_app.autodiscover_tasks()
