from django.contrib import admin
from .models import Transaction, Category, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'transaction_type', 'date']
    list_filter = ['transaction_type', 'date', 'category']
    search_fields = ['user__username', 'category__name']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'limit', 'month']
    list_filter = ['month', 'category']
    search_fields = ['user__username', 'category__name']
