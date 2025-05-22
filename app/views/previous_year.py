from datetime import date

from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from app.services.calculate_total_sum import CalculationService


def group_months_for_pagination(grouped_expenses, max_items_per_page):
    pages = []
    current_page = {}
    current_count = 0

    for month, expenses in grouped_expenses.items():
        expense_count = len(expenses)
        # Если добавление ещё одного месяца превысит лимит, то начинаем новую страницу
        if current_count + expense_count > max_items_per_page and current_page:
            pages.append(current_page)
            current_page = {}
            current_count = 0
        current_page[month] = expenses
        current_count += expense_count

    if current_page:
        pages.append(current_page)

    return pages


class PreviousYearExpensesView(TemplateView):
    template_name = 'app_html/previous-year-expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()
        previous_year = today.year - 1

        previous_year_expenses = service.get_expenses().filter(date__year=previous_year).order_by('date')
        grouped_expenses, month_total_sums, month_name_to_number = service.get_grouped_expenses(
            previous_year_expenses, previous_year
        )

        grouped_pages = group_months_for_pagination(grouped_expenses, max_items_per_page=20)
        paginator = Paginator(grouped_pages, per_page=1)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        current_grouped_expenses = page_obj.object_list[0] if page_obj.object_list else 0

        month_total_sum_not_excessive = {}
        month_percent_not_excessive = {}
        if current_grouped_expenses:
            for month_name in current_grouped_expenses.keys():
                month_number = month_name_to_number[month_name]
                value, percent = service.calculate_month_total_sum_not_excessive(month_number, previous_year)
                month_total_sum_not_excessive[month_name] = value
                month_percent_not_excessive[month_name] = percent

        context.update({
            'grouped_expenses': current_grouped_expenses,
            'previous_year': previous_year,
            'month_total_sums': month_total_sums,
            'month_total_sum_not_excessive': month_total_sum_not_excessive,
            'month_percent_not_excessive': month_percent_not_excessive,
            'year_total_sum': service.calculate_year_total_sum(previous_year),
            'year_total_sum_not_excessive': service.calculate_year_total_sum_not_excessive(previous_year)[0],
            'year_percent_not_excessive': service.calculate_year_total_sum_not_excessive(previous_year)[1],
            'page_obj': page_obj,
        })

        return context
