from django_filters import rest_framework as filters

from app.models import MonthlyBudget


class MonthlyBudgetFilter(filters.FilterSet):

    class Meta:
        model = MonthlyBudget
        fields = ['user', 'budget']
