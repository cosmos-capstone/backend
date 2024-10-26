import yfinance as yf

from django.http import JsonResponse
from django.views import View

from .models import StockPrice

class Stock(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')
        stock = yf.Ticker(symbol)
        history = stock.history(period="max")
        currency = stock.info['currency']

        for datetime, close_price in history['Close'].items():
            stock_price = StockPrice(
                symbol=symbol,
                datetime=datetime.to_pydatetime(),
                close_price=close_price,
                currency=currency
            )
            # stock_price.save()

        history_list = history.values.tolist()
        return JsonResponse({"name": stock.info['longName'], "message": history_list})
