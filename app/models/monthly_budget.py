from django.core.exceptions import ValidationError
from django.db import models

from app.mixins.model_mixins import CommonModelMixin


class MonthlyBudget(CommonModelMixin):
    budget = models.PositiveIntegerField('Бюджет на месяц', default=0)

    def clean(self):
        if not self.pk and MonthlyBudget.objects.filter(user=self.user).exists():
            raise ValidationError("Можно создать только одну запись бюджета на одного пользователя")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Бюджет на месяц'
        verbose_name_plural = 'Бюджет на месяц'
