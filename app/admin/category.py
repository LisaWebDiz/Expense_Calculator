from django.contrib import admin

from app.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    list_display_links = ('id', 'name')
    list_filter = ('user', 'name')
    search_fields = ('name',)
