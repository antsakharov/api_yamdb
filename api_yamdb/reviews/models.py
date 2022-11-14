from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    ROLE_CHOISES = [('user', 'пользователь'),
                    ('moderator', 'модератор'),
                    ('admin', 'администратор')]
    objects = CustomUserManager()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')])
    email = models.EmailField(
        max_length=254,
        unique=True)
    first_name = models.CharField(
        max_length=150,
        blank=True)
    last_name = models.CharField(
        max_length=150,
        blank=True)
    bio = models.TextField(
        blank=True)
    rule = models.CharField(
        choices=ROLE_CHOISES, default='user')

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

