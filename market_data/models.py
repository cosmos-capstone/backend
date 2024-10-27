import yfinance as yf
from datetime import timedelta

from django.db import models
from django.utils import timezone

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

        latest_db_entry = StockPrice.objects.filter(symbol=symbol).order_by('-datetime').first()

        if latest_db_entry:
            last_db_date = latest_db_entry.datetime.date()
            today_date = timezone.now().date()

            if last_db_date < today_date:
                StockPrice.fetch_and_save_stock_data(stock, symbol, start=last_db_date)
        else:
            StockPrice.fetch_and_save_stock_data(stock, symbol, period="max")

        name = stock.info['longName']
        queryset = StockPrice.objects.filter(symbol=symbol).order_by('datetime')
        currency = queryset[0].currency
        data = list(queryset.values('datetime', 'close_price'))

        return name, currency, data

    @staticmethod
    def fetch_and_save_stock_data(stock, symbol, start=None, period=None):
        if start:
            history = stock.history(start=start)
        else:
            history = stock.history(period=period)

        if history.empty:
            return

        history_datetimes = [dt.to_pydatetime() for dt in history.index]

        overlapping_entries = StockPrice.objects.filter(
            symbol=symbol,
            datetime__in=history_datetimes
        )

        if overlapping_entries.exists():
            overlapping_entries.delete()

        currency = stock.info.get('currency')

        stock_prices = [
            StockPrice(
                symbol=symbol,
                datetime=dt.to_pydatetime(),
                close_price=row['Close'],
                currency=currency
            ) for dt, row in history.iterrows()
        ]

        StockPrice.objects.bulk_create(stock_prices)
        