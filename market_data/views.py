from django.http import JsonResponse
from django.db import connections
# Create your views here.


def stock(request):
    symbol = request.GET.get('symbol')
    market_data_connection = connections['market_data']

    return JsonResponse({"message": symbol})
