from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import MonthlyBudget


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_monthly_budget_for_new_user(sender, instance, created, **kwargs):
    if created:
        MonthlyBudget.objects.create(user=instance, budget=0)
