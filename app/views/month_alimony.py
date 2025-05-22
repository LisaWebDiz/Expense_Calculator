from datetime import date

from django.views.generic.base import TemplateView

from app.services.calculate_total_sum import CalculationService
from app.services.constants import MONTHS


class MonthAlimonyView(TemplateView):
    template_name = 'app_html/month-alimony-expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        current_month = date.today().month
        month_alimony_expenses = service.get_expenses().filter(date__month=current_month, alimony=True).order_by('date')

        context['alimony_month_expenses'] = month_alimony_expenses
        context['current_month_name'] = MONTHS[current_month]
        context['sum_month_alimony_expenses'] = service.calculate_month_alimony_sum(current_month)

        return context
