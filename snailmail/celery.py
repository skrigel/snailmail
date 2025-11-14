import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snailmail.settings")
app = Celery("snailmail")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
