from datetime import date

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from app.filters import ExpenseFilter
from app.forms.expense import ExpenseForm
from app.mixins.view_mixins import UserQuerySetMixin
from app.models import Expense
from app.pagination import CustomPagination
from app.serializers.expense import ExpenseSerializer, ExpenseListRetrieveSerializer


@extend_schema(tags=['Расходы'])
@extend_schema_view(
    list=extend_schema(summary='Расходы: просмотр списка всех записей', ),
    update=extend_schema(summary='Расходы: изменение конкретной записи', ),
    partial_update=extend_schema(summary='Расходы: частичное изменение конкретной записи', ),
    create=extend_schema(summary='Расходы: создание новой записи', ),
    retrieve=extend_schema(summary='Расходы: просмотр конкретной записи', ),
    destroy=extend_schema(summary='Расходы: удаление конкретной записи', ),
)
class ExpenseViewSet(UserQuerySetMixin, ModelViewSet):
    serializer_class = ExpenseSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ExpenseFilter
    ordering_fields = ['expense', 'category', 'date']
    search_fields = ['date', 'category__name', 'expense', 'description', 'alimony', 'is_excessive']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ExpenseListRetrieveSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return ExpenseSerializer
        return ExpenseSerializer


class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'app_html/expense-add.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        print("✅ form_valid called")
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'app_html/expense-edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Ошибки формы


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('index')


class AddExpenseView(View):
    def post(self, request, *args, **kwargs):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            # Определение даты расхода
            expense_date = expense.date
            today = date.today()

            # Логика перенаправления
            if expense_date.year == today.year:
                if expense_date.month == today.month:
                    return JsonResponse({'redirect_url': None})
                elif expense_date.month == today.month - 1 or (today.month == 1 and expense_date.month == 12):
                    return JsonResponse({'redirect_url': '/app_html/previous-month-expenses/'})
            elif expense_date.year == today.year - 1:
                return JsonResponse({'redirect_url': '/app_html/previous-year-expenses/'})
            else:
                return JsonResponse({'redirect_url': '/app_html/all-time-expenses/'})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
