import base64
import io
from datetime import date

import matplotlib.pyplot as plt
from django.views.generic.base import TemplateView

from app.forms.category import CategoryForm
from app.forms.expense import ExpenseForm
from app.models import MonthlyBudget
from app.services.calculate_total_sum import CalculationService
from app.services.calculate_total_sum import calculate_remained_month_days
from app.services.constants import MONTHS


class IndexView(TemplateView):
    template_name = 'app_html/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()
        current_month = date.today().month
        current_year = date.today().year

        expenses_current_month = service.get_expenses().filter(
            date__month=current_month, date__year=current_year
        ).order_by('-date')

        monthly_budget = MonthlyBudget.objects.filter(user=self.request.user).first()
        remained = int(monthly_budget.budget) - service.calculate_month_total_sum(today.month, today.year)
        day_budget = int(remained / calculate_remained_month_days(today))

        year_value, year_percent = service.calculate_year_total_sum_not_excessive(today.year)
        month_value, month_percent = service.calculate_month_total_sum_not_excessive(
            current_month, current_year
        )

        # Группировка по категориям
        category_totals = {}
        for expense in expenses_current_month:
            category_name = expense.category.name
            category_totals[category_name] = category_totals.get(category_name, 0) + expense.expense

        # Если есть данные — диаграмма
        if category_totals:
            fig, ax = plt.subplots(figsize=(1.5, 1.5))
            ax.pie(
                category_totals.values(),
                labels=category_totals.keys(),
                autopct='%1.1f%%',
                textprops={'fontsize': 2}
            )
            ax.axis('equal')  # Круглая диаграмма

            # Сохранение в буфер
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=300)
            buf.seek(0)

            # Кодировка в base64
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()
            context['chart_base64'] = image_base64

        context['expense_form'] = ExpenseForm(user=self.request.user)
        context['category_form'] = CategoryForm()
        context['month_total_sum'] = service.calculate_month_total_sum(today.month, today.year)
        context['year_total_sum'] = service.calculate_year_total_sum(today.year)
        context['year_total_sum_not_excessive'] = year_value
        context['year_percent_not_excessive'] = year_percent
        context['month_total_sum_not_excessive'] = month_value
        context['month_percent_not_excessive'] = month_percent
        context['alimony_month_sum'] = service.calculate_month_alimony_sum(today.month)
        context['current_month_name'] = MONTHS[current_month]
        context['current_year'] = current_year
        context['expenses_current_month'] = expenses_current_month
        context['monthly_budget'] = monthly_budget
        context['remained'] = remained
        context['day_budget'] = day_budget
        return context
