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


class AllTimeExpensesView(TemplateView):
    template_name = 'app_html/all-time-expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CalculationService(self.request.user)

        all_time_expenses = service.get_expenses().order_by('-date')
        grouped_by_year, month_total_sums, month_name_to_number, month_name_to_year = \
            service.get_grouped_expenses_by_year(all_time_expenses)

        flat_grouped = {}
        for year, months in grouped_by_year.items():
            for month, expenses in months.items():
                flat_grouped[(month, year)] = expenses

        grouped_pages = group_months_for_pagination(flat_grouped, max_items_per_page=40)
        paginator = Paginator(grouped_pages, per_page=1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        current_flat_group = page_obj.object_list[0] if page_obj.object_list else 0

        nested_group = {}
        if current_flat_group:
            for (month, year), expenses in current_flat_group.items():
                nested_group.setdefault(year, {})[month] = expenses

        month_total_sum_not_excessive = {}
        month_percent_not_excessive = {}

        for month_name in month_name_to_number:
            month_number = month_name_to_number[month_name]
            year = month_name_to_year[month_name]
            value, percent = service.calculate_month_total_sum_not_excessive(month_number, year)
            month_total_sum_not_excessive[month_name] = value
            month_percent_not_excessive[month_name] = percent

        year_total_sum = {}
        year_total_sum_not_excessive = {}
        year_percent_not_excessive = {}

        for year in grouped_by_year.keys():
            year_total_sum[year] = service.calculate_year_total_sum(year)
            value, percent = service.calculate_year_total_sum_not_excessive(year)
            year_total_sum_not_excessive[year] = value
            year_percent_not_excessive[year] = percent

        context['grouped_expenses'] = nested_group
        context['page_obj'] = page_obj
        context['month_total_sums'] = month_total_sums
        context['month_total_sum_not_excessive'] = month_total_sum_not_excessive
        context['month_percent_not_excessive'] = month_percent_not_excessive
        context['year_total_sum'] = year_total_sum
        context['year_total_sum_not_excessive'] = year_total_sum_not_excessive
        context['year_percent_not_excessive'] = year_percent_not_excessive

        return context
