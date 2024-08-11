from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSACTION_TYPES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f'{self.date} - {self.category} - {self.amount}'

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.category} - {self.limit} from {self.start_date} to {self.end_date}'




