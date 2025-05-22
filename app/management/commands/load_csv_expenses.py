"""Команда для запуска 'python manage.py load_csv_expenses'"""
import csv
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import Category, Expense

User = get_user_model()


class Command(BaseCommand):
    help = "Команда для обновления таблиц"

    @atomic
    def handle(self, *args, **options):
        fixtures_path: Path = Path(settings.FIXTURE_DIRS)

        expenses_csv = fixtures_path / 'expenses.csv'
        with (open(expenses_csv, mode='r', encoding='utf-8-sig') as f):
            reader = csv.DictReader(f, dialect='excel', delimiter=';')

            for row in reader:
                user = User.objects.get(id=row['Пользователь'])

                category_obj, created = Category.objects.get_or_create(
                    user=user,
                    name=row['Категория']
                )

                def str_to_bool(value):
                    return value.lower() in ('t', 'true', '1')

                if category_obj:
                    expense_obj, created = Expense.objects.get_or_create(
                        user=user,
                        date=row['Дата'],
                        category=category_obj,
                        expense=row['Расход'],
                        description=row['Описание'],
                        alimony=str_to_bool(row['Статья алиментов']),
                        is_excessive=str_to_bool(row['Необязательный']),
                    )

        self.stdout.write(self.style.SUCCESS('Done'))
