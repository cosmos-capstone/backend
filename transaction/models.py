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
    ]

    transaction_date = models.DateTimeField(default=datetime(1970, 1, 1))
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, default='deposit')
    asset_category = models.CharField(max_length=50, choices=ASSET_CATEGORY_CHOICES, blank=True, null=True)
    stock_code = models.CharField(max_length=20, blank=True, null=True)
    stock_name = models.CharField(max_length=50, blank=True, null=True)
    bond_name = models.CharField(max_length=50, blank=True, null=True)
    fund_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    transaction_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type} - {self.asset_category} - {self.transaction_amount}"
