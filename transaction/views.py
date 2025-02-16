import json
import pytz

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from datetime import datetime
from django.http import JsonResponse
from .models import Transaction
from .utils import rebalance_asset, calculate_asset_sum, calculate_asset_sum_by_name, get_asset_totals, get_rebalanced_transaction

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

class PortfolioView(APIView):
    @extend_schema(
        summary="Get portion of portfolio",
        description="This endpoint for getting user's portion of each portfolio",
    )
    def get(self, request, *args, **kwargs):
        port_dict = calculate_asset_sum(datetime(9999, 12, 31))
        return JsonResponse({'data': port_dict})
    
class AssetView(APIView):
    @extend_schema(
        summary="Get portion of stocks",
        description="This endpoint for getting user's portion of each assets",
    )
    def get(self, request, *args, **kwargs):
        asset_dict = calculate_asset_sum_by_name()
        return JsonResponse({'data': asset_dict})

class RebalancingView(APIView):
    @extend_schema(
        summary="Get rebalanced portion of each assets",
        description=(
            "This endpoint calculates the rebalanced portion of each asset. "
            "If the `date` parameter is provided, it calculates the portion for the specified date. "
            "If not, it uses the current date."
        ),
        parameters=[
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
                description="Optional. The date for which the rebalanced portfolio should be calculated. Format: YYYY-MM-DD.",
                required=False
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        }
    )
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date', None)

        if not date_str:
            date_obj = datetime(9999, 12, 31)
        else:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        current_portfolio = calculate_asset_sum(date_obj)
        
        return JsonResponse({
            "data" : rebalance_asset(current_portfolio)
        })

class PortfolioTotalView(APIView):
    @extend_schema(
        summary="Get sum of each essets",
        description="This endpoint for getting sum of each portfolio",
    )
    def get(self, request, *args, **kwargs):
        port_dict = get_asset_totals(Transaction.objects.all().values())
        return JsonResponse({'data': port_dict})

class RebalancedTransaction(APIView):
    @extend_schema(
        summary="Get rebalenced transactions",
        parameters=[
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_obj = pytz.utc.localize(date_obj)
        current_portfolio = calculate_asset_sum(date_obj)
        rebalanced_portfolio = rebalance_asset(current_portfolio)
        
        return JsonResponse({
            "message": "success",
            "data" : get_rebalanced_transaction(rebalanced_portfolio, date_obj)
        })