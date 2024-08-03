import os
from celery import Celery
from django.core.mail import send_mail

from reviews.secret import ENVIROMENT_VARIABLES

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reviews.settings')

app = Celery('reviews')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')


@app.task(bind=True)
def task_email_send(self, username, fullname, post_url, comments, to):
    subject = f"{username} recommends you read " \
              f"{fullname}"
    message = f"Read {fullname} at {post_url}\n\n" \
              f"{username}\'s comments: {comments}"
    send_mail(subject, message, ENVIROMENT_VARIABLES['EMAIL_HOST_USER'], [to])
