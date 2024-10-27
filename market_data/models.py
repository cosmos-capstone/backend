import yfinance as yf

from django.db import models

class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    datetime = models.DateTimeField()
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.symbol} on {self.datetime}: {self.close_price}"

    @staticmethod
    def get_stock_prices(symbol):
        stock = yf.Ticker(symbol)
        # history = stock.history(period="max")
        # currency = stock.info['currency']

        # for datetime, close_price in history['Close'].items():
        #     stock_price = StockPrice(
        #         symbol=symbol,
        #         datetime=datetime.to_pydatetime(),
        #         close_price=close_price,
        #         currency=currency
        #     )
        #     stock_price.save()

        name = stock.info['longName']
        queryset = StockPrice.objects.filter(symbol=symbol).order_by('datetime')
        currency = queryset[0].currency
        data = list(queryset.values('datetime', 'close_price'))

        return name, currency, data