from django.contrib import admin
from .models import Category, Account, Transaction, Budget

admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Budget)
