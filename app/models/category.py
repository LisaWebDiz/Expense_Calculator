from django.db import models

from app.mixins.model_mixins import CommonModelMixin


class Category(CommonModelMixin):
    name = models.CharField('Категория', max_length=50)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name
