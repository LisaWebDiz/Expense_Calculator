from django import forms

from app.models import MonthlyBudget


class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
        }
