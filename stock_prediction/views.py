from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse

from .models import Prediction

class StockPrediction(APIView):
    @extend_schema(
        summary="2 Weeks stock price prediction",
        description="Load model and predict the prices of stock for 2 weeks.",
        parameters=[
            OpenApiParameter(
                name="symbol",
                type=str,
                location=OpenApiParameter.PATH,
                required=True,
                description="The stock symbol to get predicted prices (e.g., 'AAPL' for Apple Inc. and '005930.KS' for Samsung Electorinics)"
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        symbol = kwargs.get('symbol')
        prediction_dates, prediction  = Prediction.get_stock_pred(symbol)        
        return JsonResponse({"date": prediction_dates, "prediction": prediction})
