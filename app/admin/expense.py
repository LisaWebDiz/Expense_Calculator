from django.contrib import admin

from app.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'expense', 'category', 'date', 'description', 'alimony', 'is_excessive',
                    'month_category_total_sum', 'year_category_total_sum', 'total_sum', 'category_total_sum')
    list_display_links = ('id', 'expense')
    list_filter = ('user', 'category')
    search_fields = ('expense', 'category')
    ordering = ('-date',)
