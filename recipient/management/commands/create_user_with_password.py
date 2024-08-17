from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from recipient.tasks import task_email_send
from utils.pp_requests import create_pp_link
from utils.tasks_utils import run_task
from utils.text_utils import generate_password


class Command(BaseCommand):
    """Команда для создания пользователя с паролем и отправкой данных для логина на почту"""

    BATCH_SIZE = 1000

    def add_arguments(self, parser):
        """Доступные аргументы для команды"""
        parser.add_argument(
            '--delete',
            action='store_true',
            help='',
        )
        parser.add_argument('--username', type=str)
        parser.add_argument('--email', type=str)

    def handle(self, *args, **options):
        """
        Обработчик команды

        :param args: Аргументы функции
        :param options: Аргументы команды
        """
        if options['delete']:
            return
        self.create_user_with_password(username=options['username'], email=options['email'])

    def create_user_with_password(self, username, email):
        """
        Создание пользователя на сайте и отправка персональных данных на почту
        """
        self.stdout.write(self.style.WARNING('Начало создания пользователя'))

        password = generate_password()

        payload = f'Ваш логин: {username}\nВаш пароль: {password}'

        url = create_pp_link(payload, 2, 7)

        subject = 'Создан пользователь на сайте'
        message = f'Вот ссылка с вашими персональными данными для логина на сайте:\n{url}'

        self.stdout.write(
            self.style.WARNING('Команда выполняется'),
        )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        self.stdout.write(self.style.WARNING('Сохранение результата команды'))

        run_task(
            task=task_email_send,
            queue='send_email',
            task_kwargs={
                'subject': subject,
                'message': message,
                'to': [email],
            },
            task_id=f'send_mail_recipient_{user.id}',
            time_limit=60,
        )

        self.stdout.write(self.style.SUCCESS('Команда успешно выполнена'))
