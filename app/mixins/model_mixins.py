from django.conf import settings
from django.db import models


class CommonModelMixin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True
