from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from reviews.validators import validate_year


class UserRole(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    @staticmethod
    def get_all_roles():
        return tuple((i.value, i.name) for i in UserRole)


class pub_date_abstract_model(models.Model):
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
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
        choices=UserRole.get_all_roles(),
        default=UserRole.USER.value)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN.value or self.is_staff

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR.value


class Category(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=256)
    slug = models.SlugField(
        'Слаг категории',
        max_length=50,
        unique=True,
        validators=(RegexValidator(regex=r'^[-a-zA-Z0-9_]+$'),))

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Имя жанра',
        max_length=200)
    slug = models.SlugField(
        'Слаг жанра',
        unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=200)
    year = models.IntegerField(
        'Год',
        validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True)
    description = models.TextField(
        'Описание',
        max_length=255,
        null=True,
        blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр')

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(pub_date_abstract_model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1, 'Оценка не может быть меньше 1'),
                    MaxValueValidator(10, 'Оценка происходит '
                                          'по 10-ти бальной шкале')))

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(pub_date_abstract_model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
