import os
from celery import Celery
from kombu import Queue

from reviews import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviews.settings')

app = Celery('reviews')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.task_queues = (
    Queue('celery', routing_key='celery'),
    Queue('send_email', routing_key='send_email'),
)
