from django.http import JsonResponse
from django.db import connections
from django.views import View

class Stock(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')
        market_data_connection = connections['market_data']

        return JsonResponse({"message": symbol})
