from django.db import models

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
            ('deposit', 'Deposit'),
            ('withdrawal', 'Withdrawal'),
            ('buy', 'Buy'),
            ('sell', 'Sell'),
    ]

    transaction_date = models.DateTimeField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    asset_category = models.CharField(max_length=50)  # 주식, 채권, 원자재 등
    stock_code = models.CharField(max_length=20, blank=True, null=True)  # 종목코드
    stock_name = models.CharField(max_length=50, blank=True, null=True)  # 종목명
    bond_name = models.CharField(max_length=50, blank=True, null=True)  # 채권명
    fund_name = models.CharField(max_length=50, blank=True, null=True)  # 펀드명
    quantity = models.IntegerField()
    transaction_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type} - {self.asset_category} - {self.transaction_amount}"
