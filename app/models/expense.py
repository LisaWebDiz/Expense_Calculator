import datetime

from django.db import models
from django.urls import reverse

from app.mixins.model_mixins import CommonModelMixin
from app.models.category import Category


class Expense(CommonModelMixin):
    date = models.DateField('Число', default=datetime.date.today)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    expense = models.PositiveIntegerField('Расход в рублях')
    description = models.CharField('Описание', max_length=200, blank=True)
    alimony = models.BooleanField('Статья алиментов', default=False)
    is_excessive = models.BooleanField('Необязательный', default=False)

    @property
    def month_total_sum(self):
        month_expenses = Expense.objects.filter(
            date__month=self.date.month,
        )
        total_month_expenses = sum(exp.expense for exp in month_expenses)
        return total_month_expenses
    month_total_sum.fget.short_description = "Cумма расходов в этом месяце по всем категориям"

    @property
    def year_total_sum(self):
        year_expenses = Expense.objects.filter(
            date__year=self.date.year,
        )
        total_year_expenses = sum(exp.expense for exp in year_expenses)
        return total_year_expenses
    year_total_sum.fget.short_description = "Cумма расходов в этом году по всем категориям"

    @property
    def month_category_total_sum(self):
        month_category_expenses = Expense.objects.filter(
            category=self.category,
            date__year=self.date.year,
            date__month=self.date.month
        )
        total_month_category_expenses = sum(exp.expense for exp in month_category_expenses)
        return total_month_category_expenses
    month_category_total_sum.fget.short_description = "Сумма расходов в этом месяце по этой категории"

    @property
    def year_category_total_sum(self):
        year_category_expenses = Expense.objects.filter(
            category=self.category,
            date__year=self.date.year,
        )
        total_year_category_expenses = sum(exp.expense for exp in year_category_expenses)
        return total_year_category_expenses
    year_category_total_sum.fget.short_description = "Сумма расходов в этом году по этой категории"

    @property
    def total_sum(self):
        expenses = Expense.objects.all()
        total_expenses = sum(exp.expense for exp in expenses)
        return total_expenses
    total_sum.fget.short_description = "Cумма расходов за все время по всем категориям"

    @property
    def category_total_sum(self):
        category_expenses = Expense.objects.filter(category=self.category)
        total_category_expenses = sum(exp.expense for exp in category_expenses)
        return total_category_expenses
    category_total_sum.fget.short_description = "Сумма расходов за все время по этой категории"

    def get_absolute_url(self):
        return reverse('index')

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return str(self.expense)
