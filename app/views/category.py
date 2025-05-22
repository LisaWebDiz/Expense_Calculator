from django.http import JsonResponse
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from app.filters import CategoryFilter
from app.forms.category import CategoryForm
from app.mixins.view_mixins import UserQuerySetMixin
from app.models import Category
from app.pagination import CustomPagination
from app.serializers.category import CategorySerializer


@extend_schema(tags=['Категории'])
@extend_schema_view(
    list=extend_schema(summary='Категории: просмотр списка всех записей', ),
    update=extend_schema(summary='Категории: изменение конкретной записи', ),
    partial_update=extend_schema(summary='Категории: частичное изменение конкретной записи', ),
    create=extend_schema(summary='Категории: создание новой записи', ),
    retrieve=extend_schema(summary='Категории: просмотр конкретной записи', ),
    destroy=extend_schema(summary='Категории: удаление конкретной записи', ),
)
class CategoryViewSet(UserQuerySetMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CategoryFilter
    ordering_fields = ['name', ]
    search_fields = ['name', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # <-- Назначаем текущего пользователя
            category.save()
            return JsonResponse({'success': True})
        else:
            error_messages = []
            for field_errors in form.errors.values():
                error_messages.extend(field_errors)
            return JsonResponse({'success': False, 'error_message': ' '.join(error_messages)})

    return JsonResponse({'success': False, 'error_message': 'Неверный метод запроса'}, status=405)
