from django.http import JsonResponse
from django.db import connections
from django.views import View
import yfinance as yf

class Stock(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')

        stock = yf.Ticker("005930.KS")

        market_data_connection = connections['market_data']
        history = stock.history(period="max")

        history_list = history.values.tolist()
        return JsonResponse({"message": history_list})
