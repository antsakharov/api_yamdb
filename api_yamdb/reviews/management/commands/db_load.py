import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, CustomUser

FILE_MODEL = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'users': CustomUser,
    'review': Review,
    'comments': Comment,
}


class Command(BaseCommand):
    help = 'Команда для импорта данных из .csv файла в БД.' \
           'Импорт выполняется командой python manage.py db_load'

    def handle(self, *args, **options):
        for file_name, model in FILE_MODEL.items():
            with open(
                    f'static/data/{file_name}.csv',
                    newline='',
                    encoding='utf-8'
            ) as csv_file:
                datareader = csv.DictReader(csv_file, delimiter=',')
                if file_name == 'titles':
                    for row in datareader:
                        category = Category.objects.get(pk=row.pop('category'))
                        obj = model(
                            category=category,
                            **row
                        )
                        obj.save()
                elif file_name in ['review', 'comments']:
                    for row in datareader:
                        user = CustomUser.objects.get(pk=row.pop('author'))
                        obj = model(
                            author=user,
                            **row
                        )
                        obj.save()
                else:
                    model.objects.bulk_create(
                        [model(**row) for row in datareader])
        print('Импорт данных произведён успешно')
