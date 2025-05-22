from django.contrib import admin

from app.models import MonthlyBudget


@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('budget',)
    list_display_links = ('budget',)
