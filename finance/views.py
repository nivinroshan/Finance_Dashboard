from django.shortcuts import render, redirect
from .models import Transaction, Account, Category
from .forms import TransactionForm, AccountForm, CategoryForm
from django.db.models import Sum

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

    # Calculate Financial Metrics
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
 

    cash_flow = total_income - total_expenses
    
    # Assume credit transactions are marked under a specific category, e.g., 'Credit'
    total_credit = transactions.filter(category__name='Credit').aggregate(Sum('amount'))['amount__sum'] or 0
    credit_percentage = (total_credit / total_income * 100) if total_income > 0 else 0
    
    # Assume debt is also under a specific category, e.g., 'Debt'
    total_debt = transactions.filter(category__name='Debt').aggregate(Sum('amount'))['amount__sum'] or 0
    debt_percentage = (total_debt / total_income * 100) if total_income > 0 else 0

    context = {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'total_balance': total_balance,
        'transaction_form': transaction_form,
        'account_form': account_form,
        'category_form': category_form,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'cash_flow': cash_flow,
        'credit_percentage': 0,
        'debt_percentage': 0,
    }
    return render(request, 'finance/dashboard.html', context)
