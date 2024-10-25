from django.http import JsonResponse
from django.db import connections
# Create your views here.


def stock(request):
    market_data_connection = connections['market_data']
    return JsonResponse({"message": "success"})
