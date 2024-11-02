import json
import pytz
from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import JsonResponse
from .models import Transaction

@extend_schema(
    summary="Dummy Data 1",
    description="This data is for test.",
    responses={200: 'Success response'},
)
@api_view(['GET'])
def dumpdata1(request):
    return JsonResponse({"message": "success", "data": [
        {"id": 1, "transaction_date": "2023-01-01T00:00:00Z", "transaction_type": "deposit", "asset_category": None, "asset_symbol": None, "asset_name": None, "quantity": 0, "transaction_amount": "6000000.00"},
        {"id": 2, "transaction_date": "2023-05-04T13:23:00Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "SPY", "asset_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "quantity": 1, "transaction_amount": "545065.00"},
        {"id": 3, "transaction_date": "2023-06-02T12:08:00Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "SPY", "asset_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "quantity": 1, "transaction_amount": "559699.00"},
        {"id": 4, "transaction_date": "2023-09-05T13:39:00Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "SPY", "asset_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "quantity": 1, "transaction_amount": "593889.00"},
        {"id": 5, "transaction_date": "2024-04-22T23:07:48Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "VOO", "asset_name": "\ubc45\uac00\ub4dc S&P500 ETF", "quantity": 1, "transaction_amount": "672890.00"},
        {"id": 6, "transaction_date": "2024-07-30T23:08:40Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "VOO", "asset_name": "\ubc45\uac00\ub4dc S&P500 ETF", "quantity": 1, "transaction_amount": "728123.00"},
        {"id": 7, "transaction_date": "2024-01-28T23:07:20Z", "transaction_type": "buy", "asset_category": "american_stock", "asset_symbol": "QQQM", "asset_name": "\uc778\ubca0\uc2a4\ucf54 \ub098\uc2a4\ub2e5 100 ETF", "quantity": 1, "transaction_amount": "249091.00"},
        {"id": 8, "transaction_date": "2024-04-17T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "asset_symbol": "088980.KS", "asset_name": "\ub9e5\ucffc\ub9ac\uc778\ud504\ub77c", "quantity": 40, "transaction_amount": "501200.00"},
        {"id": 9, "transaction_date": "2023-12-13T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "asset_symbol": "379800.KS", "asset_name": "KODEX \ubbf8\uad6d S&P500TR", "quantity": 20, "transaction_amount": "276400.00"},
        {"id": 10, "transaction_date": "2024-02-07T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "asset_symbol": "379810.KS", "asset_name": "KODEX \ubbf8\uad6d\ub098\uc2a4\ub2e5 100TR", "quantity": 20, "transaction_amount": "313700.00"}]})

class TransactionView(APIView):
    @extend_schema(
        summary="Get all transaction data",
        description="This endpoint for getting transactions",
    )
    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse({
                    "message": "success",
                    "data": list(Transaction.objects.all().values())
                }, safe=False)

        except Exception as e:
            print(type(e), e)
            return JsonResponse({"error": str(e)}, status=400)

    @extend_schema(
        summary="Patch transaction data",
        description="This endpoint for adding transactions",
    )
    def patch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            new_transactions = []
            
            for item in data:
                is_cash = item["transaction_type"] == "deposit" or item["transaction_type"] == "withdrawal"

                if not is_cash and not item.get("asset_name"):  # asset_name이 비어 있는지 확인
                    raise Exception("Asset name이 비어있습니다.")
                if not is_cash and item.get("quantity") == 0:
                    raise Exception("Quantity가 0이 될 수 없습니다.")
                if float(item.get("transaction_amount", 0)) == 0:
                    raise Exception("Transaction amount가 0이 될 수 없습니다.")
                transaction = Transaction(
                    transaction_date=datetime.strptime(item["transaction_date"], "%Y-%m-%dT%H:%M").replace(tzinfo=pytz.timezone("Asia/Seoul")),
                    transaction_type=item["transaction_type"],
                    asset_category=item["asset_category"],
                    asset_symbol=item["asset_symbol"],
                    asset_name=item["asset_name"],
                    quantity=item["quantity"],
                    transaction_amount=item["transaction_amount"],
                )
                transaction.save()
                new_transactions.append(transaction)

            response_data = [
                {
                    "id": transaction.id,
                    "transaction_date": transaction.transaction_date.strftime("%Y-%m-%dT%H:%M"),
                    "transaction_type": transaction.transaction_type,
                    "asset_category": transaction.asset_category,
                    "asset_symbol": transaction.asset_symbol,
                    "asset_name": transaction.asset_name,
                    "quantity": transaction.quantity,
                    "transaction_amount": str(transaction.transaction_amount),
                }
                for transaction in new_transactions
            ]

            return JsonResponse(response_data, safe=False, status=201)

        except ValueError as e:
            print(type(e), e)
            return JsonResponse({"error": "날짜가 올바르지 않습니다."}, status=400)

        except Exception as e:
            print(type(e), e)
            return JsonResponse({"error": str(e)}, status=400)

    @extend_schema(
        summary="Delete transaction data",
        description="This endpoint for deleting transactions",
    )
    def delete(self, request, *args, **kwargs):
        transaction_id = request.query_params.get("id")
        
        if not transaction_id:
            return JsonResponse({"error": "Transaction ID가 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Transaction 인스턴스를 조회하고 삭제
            transaction = Transaction.objects.get(id=transaction_id)
            transaction.delete()
            
            return JsonResponse({"message": "거래 내역이 성공적으로 삭제되었습니다."})
        
        except Transaction.DoesNotExist:
            return JsonResponse({"error": "해당 ID의 거래 내역을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)