# Generated by Django 2.2.16 on 2022-11-21 17:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Оценка не может быть меньше 1'), django.core.validators.MaxValueValidator(10, 'Оценка происходит по 10-ти бальной шкале')]),
        ),
    ]
