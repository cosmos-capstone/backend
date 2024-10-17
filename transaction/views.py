from django.http import JsonResponse
from django.core import serializers
from .models import Transaction

def dumpdata1(request):
    return JsonResponse({"message": "success", "data": [{"id": 1, "transaction_date": "2023-01-01T00:00:00Z", "transaction_type": "deposit", "asset_category": None, "stock_code": None, "stock_name": None, "bond_name": None, "fund_name": None, "quantity": 0, "transaction_amount": "6000000.00"}, {"id": 2, "transaction_date": "2023-05-04T13:23:00Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "545065.00"}, {"id": 3, "transaction_date": "2023-06-02T12:08:00Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "559699.00"}, {"id": 4, "transaction_date": "2023-09-05T13:39:00Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "SPY", "stock_name": "SPDR S&P500 ETF \ud2b8\ub7ec\uc2a4\ud2b8", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "593889.00"}, {"id": 5, "transaction_date": "2024-04-22T23:07:48Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "VOO", "stock_name": "\ubc45\uac00\ub4dc S&P500 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "672890.00"}, {"id": 6, "transaction_date": "2024-07-30T23:08:40Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "VOO", "stock_name": "\ubc45\uac00\ub4dc S&P500 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "728123.00"}, {"id": 7, "transaction_date": "2024-01-28T23:07:20Z", "transaction_type": "buy", "asset_category": "american_stock", "stock_code": "QQQM", "stock_name": "\uc778\ubca0\uc2a4\ucf54 \ub098\uc2a4\ub2e5 100 ETF", "bond_name": None, "fund_name": None, "quantity": 1, "transaction_amount": "249091.00"}, {"id": 8, "transaction_date": "2024-04-17T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "stock_code": "088980", "stock_name": "\ub9e5\ucffc\ub9ac\uc778\ud504\ub77c", "bond_name": None, "fund_name": None, "quantity": 40, "transaction_amount": "501200.00"}, {"id": 9, "transaction_date": "2023-12-13T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "stock_code": "379800", "stock_name": "KODEX \ubbf8\uad6d S&P500TR", "bond_name": None, "fund_name": None, "quantity": 20, "transaction_amount": "276400.00"}, {"id": 10, "transaction_date": "2024-02-07T15:00:00Z", "transaction_type": "buy", "asset_category": "korean_stock", "stock_code": "379810", "stock_name": "KODEX \ubbf8\uad6d\ub098\uc2a4\ub2e5 100TR", "bond_name": None, "fund_name": None, "quantity": 20, "transaction_amount": "313700.00"}]})
    return JsonResponse({'message': 'success', 'data': list(Transaction.objects.values())})
