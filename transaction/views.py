from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
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
        {"id": 1, "transaction_date": "2023-01-01T00:00:00Z", "transaction_type": "deposit", "asset_category": None, "stock_code": None, "stock_name": None, "bond_name": None, "fund_name": None, "quantity": 0, "transaction_amount": "6000000.00"},
        {"id": 2, "transaction_date": "2023-05-04T13:23:00Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "545065.00"},
        {"id": 3, "transaction_date": "2023-06-02T12:08:00Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "559699.00"},
        {"id": 4, "transaction_date": "2023-09-05T13:39:00Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "593889.00"},
        {"id": 5, "transaction_date": "2024-04-22T23:07:48Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "VOO", "stock_name": "\ubc45\uac00\ub4dc S&P500 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "672890.00"},
        {"id": 6, "transaction_date": "2024-07-30T23:08:40Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "VOO", "stock_name": "\ubc45\uac00\ub4dc S&P500 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "728123.00"},
        {"id": 7, "transaction_date": "2024-01-28T23:07:20Z", "transaction_type": "buy", "asset_category": "american_stock", "symbol": "QQQM", "stock_name": "\uc778\ubca0\uc2a4\ucf54 \ub098\uc2a4\ub2e5 100 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "249091.00"},
        {"id": 8, "transaction_date": "2024-04-17T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "symbol": "088980.KS", "stock_name": "\ub9e5\ucffc\ub9ac\uc778\ud504\ub77c", "bond_name": None, "fund_name": None, "quantity": 40, "transaction_amount": "501200.00"},
        {"id": 9, "transaction_date": "2023-12-13T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "symbol": "379800.KS", "stock_name": "KODEX \ubbf8\uad6d S&P500TR", "bond_name": None, "fund_name": None, "quantity": 20, "transaction_amount": "276400.00"},
        {"id": 10, "transaction_date": "2024-02-07T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "symbol": "379810.KS", "stock_name": "KODEX \ubbf8\uad6d\ub098\uc2a4\ub2e5 100TR", "bond_name": None, "fund_name": None, "quantity": 20, "transaction_amount": "313700.00"}]})
    # return JsonResponse({'message': 'success', 'data': list(Transaction.objects.values())})

@extend_schema(
    summary="Post transaction data",
    description="This endpoint for adding transactions",
    responses={200: 'Success response'},
)
@api_view(['POST'])
def submit(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        new_transactions = []
        
        for item in data:
            transaction = Transaction(
                transaction_date=datetime.strptime(item["transaction_date"], "%Y-%m-%d"),
                transaction_type=item["transaction_type"],
                asset_category=item["asset_category"],
                stock_code=item.get("stock_code", ""),
                stock_name=item.get("stock_name", ""),
                bond_name=item.get("bond_name", ""),
                fund_name=item.get("fund_name", ""),
                quantity=item["quantity"],
                transaction_amount=item["transaction_amount"],
            )
            transaction.save()
            new_transactions.append(transaction)

        # Serialize the saved transactions
        response_data = [
            {
                "transaction_date": transaction.transaction_date.strftime("%Y-%m-%d"),
                "transaction_type": transaction.transaction_type,
                "asset_category": transaction.asset_category,
                "stock_code": transaction.stock_code,
                "stock_name": transaction.stock_name,
                "bond_name": transaction.bond_name,
                "fund_name": transaction.fund_name,
                "quantity": transaction.quantity,
                "transaction_amount": str(transaction.transaction_amount),
            }
            for transaction in new_transactions
        ]

        return JsonResponse(response_data, safe=False, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)