from django.db import models
from django.contrib.auth.models import User
import re


class Specialty(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Специальность')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Recipient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Фамилия')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    experience = models.IntegerField(default=1, verbose_name='Стаж')
    description = models.TextField(default='Описание', max_length=2000, verbose_name='Описание')
    photo = models.ImageField(default="recipient_photo/recipient.jpg", verbose_name='Фотография', null=True,
                              upload_to='recipient_photo')

    specialities = models.ManyToManyField(Specialty, related_name='recipients')

    @property
    def fullname(self):
        fullname = f'{self.second_name} {self.first_name} {self.last_name}'
        return fullname.strip()

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Обозреваемый"
        verbose_name_plural = "Обозреваемые"
        ordering = ['-second_name']
        indexes = [
            models.Index(fields=['-second_name'])
        ]


class Review(models.Model):
    original_review = models.CharField(max_length=2000, verbose_name='Исходный отзыв')
    modified_review = models.CharField(max_length=2000, verbose_name='Измененный отзыв')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    is_anonymous = models.BooleanField(default=False, verbose_name='Анонимный отзыв')
    rate = models.IntegerField(default=5, verbose_name="Оценка")

    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='reviews',
                             verbose_name='Рецензент')
    user_ip = models.GenericIPAddressField(verbose_name='Айпи адрес рецензента')
    recipient = models.ForeignKey(Recipient,
                                  null=True,
                                  on_delete=models.CASCADE,
                                  related_name='reviews',
                                  verbose_name='Обозреваемый')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create'])
        ]

    def __str__(self):
        return self.modified_review

    def save(self, *args, **kwargs):
        self.modified_review = str(self.original_review)
        super().save(*args, **kwargs)
