import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models

ROLE_CHOIСES = [('user', 'пользователь'),
                ('moderator', 'модератор'),
                ('admin', 'администратор')]

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')])
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
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOIСES,
        default='user')

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=256
    )
    slug = models.SlugField(
        'слаг категории',
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'имя жанра',
        max_length=200
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
    )
    year = models.IntegerField(
        'год',
        validators=[MaxValueValidator(datetime.date.today().year, 'Неверно введен год')]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

