from rest_framework import serializers

from app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name']

    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Category.objects.all(),
            fields=('user', 'name'),
            message='Такая категория уже существует'
        )
    ]
