from celery import Celery

import os

app = Celery("taskforge")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskforge.settings")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()