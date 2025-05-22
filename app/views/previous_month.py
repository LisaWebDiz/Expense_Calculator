from datetime import date

from django.views.generic.base import TemplateView

from app.services.calculate_total_sum import CalculationService
from app.services.calculate_total_sum import get_previous_month
from app.services.constants import MONTHS


class PreviousMonthExpensesView(TemplateView):
    template_name = 'app_html/previous-month-expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()

        previous_month = get_previous_month(today)
        previous_month_expenses = service.get_expenses().filter(date__month=previous_month).order_by('date')
        year = today.year - 1 if previous_month == 12 else today.year

        month_value, month_percent = service.calculate_month_total_sum_not_excessive(previous_month, year)

        context['previous_month_expenses'] = previous_month_expenses
        context['previous_month_name'] = MONTHS[previous_month]
        context['month_total_sum'] = service.calculate_month_total_sum(previous_month, year)
        context['month_total_sum_not_excessive'] = month_value
        context['month_percent_not_excessive'] = month_percent

        return context
