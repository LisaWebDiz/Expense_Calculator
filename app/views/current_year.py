from datetime import date

from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from app.services.calculate_total_sum import CalculationService


def group_months_for_pagination(grouped_expenses, max_items_per_page=40):
    pages = []
    current_page = {}
    current_count = 0
    month_to_page = {}
    page_index = 1

    for month, expenses in grouped_expenses.items():
        expense_count = len(expenses)
        if current_count + expense_count > max_items_per_page and current_page:
            pages.append(current_page)
            page_index += 1
            current_page = {}
            current_count = 0
        current_page[month] = expenses
        current_count += expense_count
        month_to_page[month] = page_index

    if current_page:
        pages.append(current_page)

    return pages, month_to_page


class CurrentYearExpensesView(TemplateView):
    template_name = 'app_html/current-year-expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)
        today = date.today()
        current_year = today.year

        current_year_expenses = service.get_expenses().filter(date__year=current_year).order_by('date')
        grouped_expenses, month_total_sums, month_name_to_number = service.get_grouped_expenses(
            current_year_expenses, current_year
        )
        paginated_months, month_to_page = group_months_for_pagination(grouped_expenses)

        paginator = Paginator(paginated_months, per_page=1)  # каждый элемент = 1 блок из нескольких месяцев
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        current_group = page_obj.object_list[0] if page_obj.object_list else None

        month_total_sum_not_excessive = {}
        month_percent_not_excessive = {}
        if current_group:
            for month_name in current_group.keys():
                month_number = month_name_to_number[month_name]
                value, percent = service.calculate_month_total_sum_not_excessive(month_number, current_year)
                month_total_sum_not_excessive[month_name] = value
                month_percent_not_excessive[month_name] = percent

        context.update({
            'month_to_page': month_to_page,
            'grouped_expenses': current_group,
            'month_total_sums': month_total_sums,
            'month_total_sum_not_excessive': month_total_sum_not_excessive,
            'month_percent_not_excessive': month_percent_not_excessive,
            'year_total_sum': service.calculate_year_total_sum(current_year),
            'year_total_sum_not_excessive': service.calculate_year_total_sum_not_excessive(current_year)[0],
            'year_percent_not_excessive': service.calculate_year_total_sum_not_excessive(current_year)[1],
            'page_obj': page_obj,
            'current_year': current_year,
        })
        return context
