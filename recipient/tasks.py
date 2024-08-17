from django.core.mail import send_mail

from reviews.celery import app
from reviews.secret import ENVIROMENT_VARIABLES


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')


@app.task(bind=True)
def task_email_send(self, subject, message, to):

    send_mail(subject, message, ENVIROMENT_VARIABLES['EMAIL_HOST_USER'], to)
