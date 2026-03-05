from django.contrib import admin
from .models import Category, Transaction, Budget

# Register your models here so they appear in the Django admin panel.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)