from datetime import date

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from app.models import Expense, Category
from app.services.calculate_total_sum import CalculationService
from app.services.calculate_total_sum import get_previous_month, calculate_percent_of_total_sum


class InfoView(TemplateView):
    template_name = 'app_html/info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()
        current_year = today.year
        previous_year = today.year - 1
        previous_month = get_previous_month(today)
        year = today.year - 1 if previous_month == 12 else today.year
        last_year_same_month = date(today.year - 1, today.month, 1)

        # Получение ID категории из URL
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        # Если категория найдена, фильтрация расходов по категории
        if category_id:
            expenses_for_category = Expense.objects.filter(category_id=category_id).order_by('-date')
        else:
            expenses_for_category = Expense.objects.none()

        month_category_expenses = service.calculate_month_category_total_sum(today.month, today.year, category)

        previous_month_category_expenses = service.calculate_month_category_total_sum(previous_month, year, category)

        last_year_same_month_category_expenses = service.calculate_month_category_total_sum(
            last_year_same_month.month, previous_year, category
        )

        _, current_year_avg_monthly_expense = service.calculate_year_category_avg_monthly(current_year, category)
        year_months_with_expenses, _ = service.calculate_year_category_avg_monthly(current_year, category)

        _, previous_year_avg_monthly_expense = service.calculate_year_category_avg_monthly(previous_year, category)

        _, all_time_avg_monthly_expense = service.calculate_category_avg(category)
        months_with_expenses, _ = service.calculate_category_avg(category)

        current_year_category_expenses = service.calculate_year_category_total_sum(current_year, category)

        previous_year_category_expenses = service.calculate_year_category_total_sum(previous_year, category)

        all_time_category_expenses = service.calculate_category_total_sum(category)

        context['category_name'] = category.name

        context['month_category_expenses'] = month_category_expenses
        context['percent_of_month_category_expenses'] = calculate_percent_of_total_sum(
            month_category_expenses, service.calculate_month_total_sum(today.month, today.year)
        )

        context['previous_month_category_expenses'] = previous_month_category_expenses
        context['percent_of_previous_month_category_expenses'] = calculate_percent_of_total_sum(
            previous_month_category_expenses, service.calculate_month_total_sum(previous_month, year)
        )

        context['last_year_same_month_category_expenses'] = last_year_same_month_category_expenses
        context['percent_of_last_year_same_month_category_expenses'] = calculate_percent_of_total_sum(
            last_year_same_month_category_expenses,
            service.calculate_month_total_sum(last_year_same_month.month, previous_year)
        )

        context['current_year_avg_monthly_expense'] = current_year_avg_monthly_expense
        context['percent_of_current_year_avg_monthly_expense'] = calculate_percent_of_total_sum(
            current_year_avg_monthly_expense,
            (service.calculate_year_total_sum(current_year) / year_months_with_expenses)
        )

        context['previous_year_avg_monthly_expense'] = previous_year_avg_monthly_expense
        context['percent_of_previous_year_avg_monthly_expense'] = calculate_percent_of_total_sum(
            previous_year_avg_monthly_expense,
            (service.calculate_year_total_sum(previous_year) / service.check_month_year_entries(previous_year))
            if service.check_month_year_entries(previous_year) else 0
        )

        context['all_time_avg_monthly_expense'] = all_time_avg_monthly_expense
        context['percent_of_all_time_avg_monthly_expense'] = calculate_percent_of_total_sum(
            all_time_avg_monthly_expense,
            service.calculate_total_sum() / months_with_expenses
        )

        context['current_year_category_expenses'] = current_year_category_expenses
        context['percent_of_current_year_category_expenses'] = calculate_percent_of_total_sum(
            current_year_category_expenses, service.calculate_year_total_sum(current_year)
        )

        context['previous_year_category_expenses'] = previous_year_category_expenses
        context['percent_of_previous_year_category_expenses'] = calculate_percent_of_total_sum(
            previous_year_category_expenses, service.calculate_year_total_sum(previous_year)
        )

        context['all_time_category_expenses'] = all_time_category_expenses
        context['percent_of_all_time_expenses'] = calculate_percent_of_total_sum(
            all_time_category_expenses, service.calculate_total_sum()
        )

        return context
