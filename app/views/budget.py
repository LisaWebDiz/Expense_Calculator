from django.http import JsonResponse
from django.views.generic import UpdateView
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from app.filters import MonthlyBudgetFilter
from app.forms.budget import MonthlyBudgetForm
from app.mixins.view_mixins import UserQuerySetMixin
from app.models import MonthlyBudget
from app.pagination import CustomPagination
from app.serializers.monthly_budget import MonthlyBudgetSerializer


class MonthlyBudgetUpdateView(UpdateView):
    model = MonthlyBudget
    form_class = MonthlyBudgetForm

    template_name = 'app_html/budget-edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})  # Успешный ответ JSON

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)  # Ошибки формы


@extend_schema(tags=['Бюджет на месяц'])
@extend_schema_view(
    list=extend_schema(summary='Бюджет на месяц: просмотр списка всех записей', ),
    update=extend_schema(summary='Бюджет на месяц: изменение конкретной записи', ),
    partial_update=extend_schema(summary='Бюджет на месяц: частичное изменение конкретной записи', ),
    create=extend_schema(summary='Бюджет на месяц: создание новой записи', ),
    retrieve=extend_schema(summary='Бюджет на месяц: просмотр конкретной записи', ),
    destroy=extend_schema(summary='Бюджет на месяц: удаление конкретной записи', ),
)
class MonthlyBudgetViewSet(UserQuerySetMixin, ModelViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = MonthlyBudgetSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = MonthlyBudgetFilter
    ordering_fields = ['budget', ]
    search_fields = ['budget', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
