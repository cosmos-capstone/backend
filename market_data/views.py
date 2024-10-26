from django.http import JsonResponse
from django.views import View
import yfinance as yf

class Stock(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')
        stock = yf.Ticker(symbol)
        history = stock.history(period="max")

        history_list = history.values.tolist()
        return JsonResponse({"name": stock.info['longName'], "message": history_list})
