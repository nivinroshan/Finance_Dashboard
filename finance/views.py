from django.shortcuts import render, redirect
from .models import Transaction, Account, Category
from .forms import TransactionForm, AccountForm, CategoryForm

def dashboard(request):
    # transactions = Transaction.objects.all()
    # accounts = Account.objects.all()
    # categories = Category.objects.all()
    # total_balance = sum(account.balance for account in accounts)

    transaction_form = TransactionForm()
    account_form = AccountForm()
    category_form = CategoryForm()

    if request.method == 'POST':
        if 'transaction_form' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction=transaction_form.save(commit=False)
                # Update the account balance based on the transaction type
                if transaction.type == 'income':
                    transaction.account.balance += transaction.amount
                elif transaction.type == 'expense':
                    transaction.account.balance -= transaction.amount
                
                transaction.save()
                transaction.account.save()

                return redirect('dashboard')
        
        elif 'account_form' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account_form.save()
                return redirect('dashboard')
        elif 'category_form' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('dashboard')
    else:
        transaction_form = TransactionForm()
        account_form = AccountForm()
        category_form = CategoryForm()
        
    # Fetch the data to display on the dashboard
    transactions = Transaction.objects.all()
    accounts = Account.objects.all()
    categories = Category.objects.all()
    total_balance = sum(account.balance for account in accounts)

    context = {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'total_balance': total_balance,
        'transaction_form': transaction_form,
        'account_form': account_form,
        'category_form': category_form,
    }
    return render(request, 'finance/dashboard.html', context)
