import calendar
from datetime import date
from decimal import Decimal
from itertools import groupby

from django.db.models import Sum
from django.db.models import functions

from app.models import Expense
from app.services.constants import MONTHS


def get_previous_month(today=None):
    """ Возвращает предыдущий месяц """
    if today is None:
        today = date.today()

    if today.month == 1:
        previous_month = 12
    else:
        previous_month = today.month - 1

    return previous_month


def calculate_percent_of_total_sum(amount, total):
    """ Рассчитывает процент от суммы """
    if amount and total > 0:
        return round(float((amount / total) * 100))
    else:
        return 0


def calculate_remained_month_days(today):
    """ Определяет количество дней, оставшихся до конца месяца, включая сегодняшний """
    _, days_in_month = calendar.monthrange(today.year, today.month)
    days_left_including_today = days_in_month - today.day + 1

    return days_left_including_today


def check_non_full_month(months_with_expenses):
    """ Определяет завершенные месяцы, в которых были расходы  """
    today = date.today()
    year, month, day = today.year, today.month, today.day
    last_month_day = calendar.monthrange(year, month)[1]
    if today != last_month_day:
        day_of_year = today.timetuple().tm_yday
        all_decimal_months = Decimal(day_of_year) / Decimal(365) * Decimal(12)
        fractional_part = all_decimal_months - all_decimal_months.to_integral_value()
        months_with_expenses -= 1 + fractional_part
    return months_with_expenses


class CalculationService:
    def __init__(self, user):
        self.user = user

    def get_expenses(self):
        return Expense.objects.filter(user=self.user)

    def calculate_total_sum(self):
        """ Рассчитывает общую сумму расходов за все время """
        all_time_expenses = Expense.objects.filter(
            user=self.user
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return all_time_expenses

    def calculate_year_total_sum(self, year):
        """ Рассчитывает общую сумму расходов за указанный год """
        year_expenses = Expense.objects.filter(
            user=self.user,
            date__year=year
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return year_expenses

    def calculate_year_total_sum_not_excessive(self, year):
        """ Рассчитывает сумму обязательных расходов за указанный год и процент от общей суммы расходов этого года """
        year_expenses_not_excessive = Expense.objects.filter(
            user=self.user,
            date__year=year,
            is_excessive=False).aggregate(
            Sum('expense')
        )['expense__sum'] or 0

        year_expenses_not_excessive_percent = year_expenses_not_excessive * 100 / self.calculate_year_total_sum(year) \
            if self.calculate_year_total_sum(year) else 0
        return year_expenses_not_excessive, int(year_expenses_not_excessive_percent)

    def calculate_month_total_sum(self, month, year):
        """ Рассчитывает общую сумму расходов за указанный месяц года """
        month_expenses = Expense.objects.filter(
            user=self.user,
            date__month=month,
            date__year=year
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return month_expenses

    def calculate_month_total_sum_not_excessive(self, month, year):
        """ Рассчитывает сумму обязательных расходов за указанный месяц года
        и процент от общей суммы расходов этого месяца """
        month_expenses_not_excessive = Expense.objects.filter(
            user=self.user,
            date__month=month,
            date__year=year,
            is_excessive=False).aggregate(
            Sum('expense')
        )['expense__sum'] or 0

        month_expenses_not_excessive_percent = month_expenses_not_excessive * 100 / self.calculate_month_total_sum(
            month, year
        ) if self.calculate_month_total_sum(
            month, year
        ) else 0
        return month_expenses_not_excessive, int(month_expenses_not_excessive_percent)

    def calculate_category_total_sum(self, category):
        """ Рассчитывает общую сумму расходов по категории за все время """
        all_category_expenses = Expense.objects.filter(
            user=self.user,
            category=category
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return all_category_expenses

    def calculate_year_category_total_sum(self, year, category):
        """ Рассчитывает общую сумму расходов по категории за указанный год """
        year_category_expenses = Expense.objects.filter(
            user=self.user,
            date__year=year,
            category=category
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return year_category_expenses

    def calculate_month_category_total_sum(self, month, year, category):
        """ Рассчитывает общую сумму расходов по категории за указанный месяц и год """
        month_category_expenses = Expense.objects.filter(
            user=self.user,
            date__month=month,
            date__year=year,
            category=category
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return month_category_expenses

    def check_month_year_entries(self, year):
        """ Определяет месяцы, по которым есть записи расходов в определенном году """
        months_with_expenses = len(set(
            Expense.objects.filter(user=self.user, date__year=year)
            .annotate(month=functions.ExtractMonth('date'))
            .values_list('month', flat=True)
            .distinct()
        ))
        return months_with_expenses

    def calculate_category_avg(self, category):
        """ Рассчитывает среднее арифметическое трат по категории в месяц за все время """
        expenses = self.calculate_category_total_sum(category)
        months_with_expenses = len(set(
            Expense.objects.filter(user=self.user)
            .annotate(
                year=functions.ExtractYear('date'), month=functions.ExtractMonth('date')
            ).values_list('year', 'month').distinct()
        ))

        months_with_expenses = check_non_full_month(months_with_expenses)
        avg_monthly_expense = expenses / months_with_expenses if months_with_expenses > 0 else 0
        return months_with_expenses, round(avg_monthly_expense)

    def calculate_year_category_avg_monthly(self, year, category):
        """ Рассчитывает среднее арифметическое трат по категории в месяц за указанный год """
        expenses = self.calculate_year_category_total_sum(year, category)

        year_months_with_expenses = self.check_month_year_entries(year)
        today = date.today()
        if year == today.year:
            year_months_with_expenses = check_non_full_month(year_months_with_expenses)

        avg_monthly_expense = expenses / year_months_with_expenses if year_months_with_expenses > 0 else 0

        return year_months_with_expenses, round(avg_monthly_expense)

    def calculate_month_alimony_sum(self, month):
        """ Рассчитывает сумму расходов по статье алиментов за указанный месяц """
        alimony_month_expenses = Expense.objects.filter(
            user=self.user,
            date__month=month,
            alimony=True
        ).aggregate(Sum('expense'))['expense__sum'] or 0
        return alimony_month_expenses

    def get_grouped_expenses_by_year(self, expenses):
        """ Группирует расходы по годам и месяцам """
        grouped_by_year = {}
        month_name_to_number = {}
        month_name_to_year = {}
        month_to_number = {month: index for index, month in enumerate(MONTHS) if month}

        for year, expenses_by_year in groupby(expenses, key=lambda x: x.date.year):
            grouped_by_month = {}
            for key, group in groupby(expenses_by_year, key=lambda x: x.date.strftime("%Y-%m")):
                year_str, month = key.split('-')
                month_name = f"{MONTHS[int(month)]} {year_str}"
                grouped_by_month[month_name] = list(group)
                month_name_to_number[month_name] = int(month)
                month_name_to_year[month_name] = int(year_str)
            grouped_by_year[year] = grouped_by_month

        month_total_sums = {}
        for year, months in grouped_by_year.items():
            for month_name, expenses in months.items():
                month_name_parts = month_name.split()

                if len(month_name_parts) == 2:
                    month = month_name_parts[0]
                    year_str = month_name_parts[1]
                else:
                    print(f"Ошибка формата month_name: {month_name}")
                    continue

                month_number = month_to_number.get(month)

                if month_number is not None:
                    month_total_sums[month_name] = self.calculate_month_total_sum(month_number, int(year_str))
                else:
                    print(f"Месяц {month} не найден в month_to_number")

        return grouped_by_year, month_total_sums, month_name_to_number, month_name_to_year

    def get_grouped_expenses(self, expenses, target_year):
        """ Группирует расходы года по месяцам """
        grouped_expenses = {}
        month_to_number = {month: index for index, month in enumerate(MONTHS) if month}
        month_name_to_number = {}

        for key, group in groupby(expenses, key=lambda x: x.date.strftime("%Y-%m")):
            year, month = key.split('-')
            month_name = f"{MONTHS[int(month)]} {year}"
            grouped_expenses[month_name] = list(group)
            month_name_to_number[month_name] = int(month)

        month_total_sums = {}
        for month_name, expenses in grouped_expenses.items():
            month = month_name.split()[0]
            year = int(month_name.split()[1])
            month_number = month_to_number[month]
            month_total_sums[month_name] = self.calculate_month_total_sum(month_number, target_year)

        return grouped_expenses, month_total_sums, month_name_to_number
