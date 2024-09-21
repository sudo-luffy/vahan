import os
from celery import shared_task
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("vahan")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.task_routes = {
    "core.celery.debug_task": {"queue": "celery"},
    "core.tasks.process_csv_task": {"queue": "celery"},
}

@shared_task
def debug_task(self):
    print("debug task")

