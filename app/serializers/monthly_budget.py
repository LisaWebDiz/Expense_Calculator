from rest_framework import serializers

from app.models import MonthlyBudget


class MonthlyBudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyBudget
        fields = ['id', 'user', 'budget']
