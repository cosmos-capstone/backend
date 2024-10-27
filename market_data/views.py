from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse

from .models import StockPrice

class Stock(APIView):
    @extend_schema(
        summary="Get Stock Prices",
        description="Fetches stock prices for a given symbol, including name, currency, and historical data.",
        parameters=[
            OpenApiParameter(
                name="symbol",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The stock symbol for which to retrieve prices (e.g., 'AAPL' for Apple Inc. and '005930.KS' for Samsung Electorinics)"
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol')
        name, currency, data = StockPrice.get_stock_prices(symbol)
        return JsonResponse({"name": name, "currency": currency, "data": data})
