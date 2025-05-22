from django import forms

from app.models import Expense, Category


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'expense': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'alimony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_excessive': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
