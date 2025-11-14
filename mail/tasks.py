from celery import shared_task
from django.utils import timezone


@shared_task
def ping():
    return f"pong at {timezone.now().isoformat()}"