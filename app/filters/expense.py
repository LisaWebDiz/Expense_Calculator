from django_filters import rest_framework as filters

from app.models import Expense, Category


class ExpenseFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='date')

    category = filters.ModelChoiceFilter(
        queryset=Category.objects.none()
    )

    class Meta:
        model = Expense
        fields = ['user', 'date', 'category', 'expense', 'description', 'alimony', 'is_excessive']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_id = self.data.get('user')
        if user_id:
            try:
                self.filters['category'].queryset = Category.objects.filter(user_id=user_id)
            except (ValueError, TypeError):
                self.filters['category'].queryset = Category.objects.none()
