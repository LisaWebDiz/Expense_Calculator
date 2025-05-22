from rest_framework import serializers

from app.models import Expense
from app.serializers.category import CategorySerializer


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'date', 'category', 'expense', 'description', 'alimony', 'is_excessive']


class ExpenseListRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'date', 'category', 'expense', 'description', 'alimony', 'is_excessive',
                  'month_total_sum', 'year_total_sum', 'month_category_total_sum', 'year_category_total_sum',
                  'total_sum', 'category_total_sum']
