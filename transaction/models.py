from django.db import models
from datetime import datetime

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    ASSET_CATEGORY_CHOICES = [
        ('korean_stock', 'Korean Stock'),
        ('american_stock', 'American Stock'),
        ('korean_bond', 'Korean Bond'),
        ('american_bond', 'American Bond'),
        ('commodity', 'Commodity'),
        ('gold', 'Gold'),
        ('deposit', 'Deposit'),
        ('savings', 'Savings Account'),
    ]

    # Common fields
    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    asset_category = models.CharField(max_length=50, choices=ASSET_CATEGORY_CHOICES)

    # For stock
    stock_code = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=50)

    # For bond
    bond_name = models.CharField(max_length=50)

    # For fund
    fund_name = models.CharField(max_length=50)

    # Common fields
    quantity = models.IntegerField(default=0)
    transaction_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type} - {self.asset_category} - {self.transaction_amount}"
