# Generated by Django 5.0.1 on 2025-01-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_category_category_name_alter_expense_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense',
            field=models.PositiveIntegerField(verbose_name='Расход в рублях'),
        ),
    ]
