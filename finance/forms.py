from django import forms
from .models import Transaction, Account, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'account', 'amount', 'date', 'description', 'type']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
