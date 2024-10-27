from django.http import JsonResponse
from django.views import View

from .models import StockPrice

class Stock(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')
        name, currency, data = StockPrice.get_stock_prices(symbol)
        return JsonResponse({"name": name, "currency": currency, "data": data})
