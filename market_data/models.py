from django.db import models

class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    datetime = models.DateTimeField()
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.symbol} on {self.datetime}: {self.close_price}"