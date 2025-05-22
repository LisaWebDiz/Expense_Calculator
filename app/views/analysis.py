from datetime import date

from django.views.generic.base import TemplateView

from app.models import Category
from app.services.calculate_total_sum import CalculationService
from app.services.calculate_total_sum import get_previous_month, calculate_percent_of_total_sum


class AnalysisView(TemplateView):
    template_name = 'app_html/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()
        current_year = today.year
        previous_year = today.year - 1
        previous_month = get_previous_month(today)
        year = today.year - 1 if previous_month == 12 else today.year
        last_year_same_month = date(today.year - 1, today.month, 1)

        categories = Category.objects.filter(user=self.request.user)

        category_data = []
        for category in categories:
            name = category.name
            month_category_expenses = service.calculate_month_category_total_sum(
                today.month, today.year, category)
            percent_of_month_category_expenses = calculate_percent_of_total_sum(
                month_category_expenses, service.calculate_month_total_sum(today.month, today.year)
            )
            previous_month_category_expenses = service.calculate_month_category_total_sum(
                previous_month, year, category
            )
            percent_of_previous_month_category_expenses = calculate_percent_of_total_sum(
                previous_month_category_expenses, service.calculate_month_total_sum(previous_month, year)
            )
            last_year_same_month_category_expenses = service.calculate_month_category_total_sum(
                last_year_same_month.month, previous_year, category
            )
            percent_of_last_year_same_month_category_expenses = calculate_percent_of_total_sum(
                last_year_same_month_category_expenses,
                service.calculate_month_total_sum(last_year_same_month.month, previous_year)
            )
            _, current_year_avg_monthly_expense = service.calculate_year_category_avg_monthly(current_year, category)
            year_months_with_expenses, _ = service.calculate_year_category_avg_monthly(current_year, category)
            percent_of_current_year_avg_monthly_expense = calculate_percent_of_total_sum(
                current_year_avg_monthly_expense, (service.calculate_year_total_sum(current_year) /
                                                   year_months_with_expenses)
            )
            _, previous_year_avg_monthly_expense = service.calculate_year_category_avg_monthly(previous_year, category)
            percent_of_previous_year_avg_monthly_expense = calculate_percent_of_total_sum(
                previous_year_avg_monthly_expense,
                (service.calculate_year_total_sum(previous_year) / service.check_month_year_entries(previous_year))
                if service.check_month_year_entries(previous_year) else 0)

            _, all_time_avg_monthly_expense = service.calculate_category_avg(category)
            months_with_expenses, _ = service.calculate_category_avg(category)
            percent_of_all_time_avg_monthly_expense = calculate_percent_of_total_sum(
                all_time_avg_monthly_expense, service.calculate_total_sum() / months_with_expenses
            )
            current_year_category_expenses = service.calculate_year_category_total_sum(current_year, category)
            percent_of_current_year_category_expenses = calculate_percent_of_total_sum(
                current_year_category_expenses, service.calculate_year_total_sum(current_year)
            )
            previous_year_category_expenses = service.calculate_year_category_total_sum(previous_year, category)
            percent_of_previous_year_category_expenses = calculate_percent_of_total_sum(
                previous_year_category_expenses, service.calculate_year_total_sum(previous_year)
            )
            all_time_category_expenses = service.calculate_category_total_sum(category)
            percent_of_all_time_expenses = calculate_percent_of_total_sum(
                all_time_category_expenses, service.calculate_total_sum()
            )
            category_data.append({
                'name': name,
                'category': category,
                'month_category_expenses': month_category_expenses,
                'percent_of_month_category_expenses': percent_of_month_category_expenses,
                'previous_month_category_expenses': previous_month_category_expenses,
                'percent_of_previous_month_category_expenses': percent_of_previous_month_category_expenses,
                'last_year_same_month_category_expenses': last_year_same_month_category_expenses,
                'percent_of_last_year_same_month_category_expenses': percent_of_last_year_same_month_category_expenses,
                'current_year_avg_monthly_expense': current_year_avg_monthly_expense,
                'percent_of_current_year_avg_monthly_expense': percent_of_current_year_avg_monthly_expense,
                'previous_year_avg_monthly_expense': previous_year_avg_monthly_expense,
                'percent_of_previous_year_avg_monthly_expense': percent_of_previous_year_avg_monthly_expense,
                'all_time_avg_monthly_expense': all_time_avg_monthly_expense,
                'percent_of_all_time_avg_monthly_expense': percent_of_all_time_avg_monthly_expense,
                'current_year_category_expenses': current_year_category_expenses,
                'percent_of_current_year_category_expenses': percent_of_current_year_category_expenses,
                'previous_year_category_expenses': previous_year_category_expenses,
                'percent_of_previous_year_category_expenses': percent_of_previous_year_category_expenses,
                'all_time_category_expenses': all_time_category_expenses,
                'percent_of_all_time_expenses': percent_of_all_time_expenses,
            })

        context['categories'] = categories
        context['category_data'] = category_data

        return context
