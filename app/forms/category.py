from django import forms

from app.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'})
        }
