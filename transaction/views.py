import json
import pytz
from datetime import datetime, timedelta
import FinanceDataReader as fdr
import numpy as np

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema
from decimal import Decimal
from django.http import JsonResponse
from .models import Transaction
from .utils import calculate_asset_sum, calculate_asset_sum_by_name, get_asset_totals


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

class PortfolioView(APIView):
    @extend_schema(
        summary="Get portion of portfolio",
        description="This endpoint for getting user's portion of each portfolio",
    )
    def get(self, request, *args, **kwargs):
        port_dict = calculate_asset_sum()
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
        description="This endpoint for getting rebalanced portion of each assets",
    )
    def get(self, request, *args, **kwargs):
        current_portfolio = calculate_asset_sum()
        # sharp ratio of stock 3-Q : K=-0.07, A=1.99,   
        # sharp ratio of bond 3-Q : K=0.79, A=0.05,
        
        # K/A deposit interest rate
        risk_free_rate = 0.022
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        
        kospi = fdr.DataReader('KS11', start_date, end_date)  # KOSPI
        nasdaq = fdr.DataReader('IXIC', start_date, end_date)  # NASDAQ

        kospi_1y_return = (kospi['Close'][-1] / kospi['Close'][0]) - 1
        nasdaq_1y_return = (nasdaq['Close'][-1] / nasdaq['Close'][0]) - 1
        num_days = len(kospi['Close'].dropna())

        kospi_std_dev = kospi['Close'].pct_change().std() * np.sqrt(num_days)
        nasdaq_std_dev = nasdaq['Close'].pct_change().std() * np.sqrt(num_days)

        sharpe_ratios = {
            'korean_stock': (kospi_1y_return - risk_free_rate) / kospi_std_dev,
            'american_stock': (nasdaq_1y_return - risk_free_rate) / nasdaq_std_dev,
            'korean_bond': 0.79, 
            'american_bond': 0.05,
            'fund': 0.3,  # 2024 ratio
            'commodity': 0.2, #2024 ratio
            'gold': 0.2,  # 2024 ratio
            'deposit': risk_free_rate
        }
        total_sharpe = sum(sharpe_ratios.values())
        target_portfolio = {asset: round((sharpe / total_sharpe)*100,2) for asset, sharpe in sharpe_ratios.items()}
        
        weight_current = Decimal(0.7)
        weight_target = Decimal(0.3)
        
        final_portfolio = {
    asset: round(Decimal(str(current_portfolio.get(asset, 0))) * weight_current + 
                 Decimal(str(target_portfolio.get(asset, 0))) * weight_target, 2)
    for asset in set(current_portfolio) | set(target_portfolio)
}
        
        return JsonResponse({
            "data" : final_portfolio
        })

class PortfolioTotalView(APIView):
    @extend_schema(
        summary="Get sum of each essets",
        description="This endpoint for getting sum of each portfolio",
    )
    def get(self, request, *args, **kwargs):
        port_dict = get_asset_totals()
        return JsonResponse({'data': port_dict})