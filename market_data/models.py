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

        try:
            name = stock.info['longName']
        except Exception as e:
            raise Exception(symbol + " not found.")
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
        
    @staticmethod
    def get_latest_price_before(symbol, datetime):
        """
        symbol과 datetime을 받아서 datetime 이전의 가장 최신 close_price와 currency를 반환.
        데이터가 없으면 fetch_and_save_stock_data(symbol)를 호출한 뒤 다시 조회.
        """
        # Step 1: 가장 최신 데이터 조회
        latest_record = StockPrice.objects.filter(symbol=symbol, datetime__lt=datetime).order_by('-datetime').first()
        
        if latest_record:
            return latest_record.close_price, latest_record.currency
        
        # Step 2: 데이터가 없을 경우 fetch_and_save_stock_data 호출
        stock = yf.Ticker(symbol)
        StockPrice.fetch_and_save_stock_data(stock, symbol)
        
        # Step 3: 다시 데이터 조회
        latest_record = StockPrice.objects.filter(symbol=symbol, datetime__lt=datetime).order_by('-datetime').first()
        
        if latest_record:
            return latest_record.close_price, latest_record.currency
        
        # Step 4: fetch_and_save_stock_data 호출 후에도 데이터가 없는 경우 예외 처리
        raise ValueError(f"No stock data available for symbol {symbol} before {datetime}.")