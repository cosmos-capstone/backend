# utils.py
from .models import Transaction

def calculate_asset_sum():
    all_data = Transaction.objects.all().values()
    print(all_data)
    asset_dict = {
        'korean_stock': 0,
        'american_stock': 0,
        'korean_bond': 0,
        'american_bond': 0,
        'fund': 0,
        'commodity': 0,
        'gold': 0,
        'deposit': 0,
        'cash': 0,
    }
    
    for data in all_data:
        total_transaction_value = data['transaction_amount'] * data['quantity']
        total_cash_value = data["transaction_amount"]  # quantity of deposit and withdrawal is always 0

        if data['transaction_type'] == 'deposit':
            asset_dict['cash'] += total_cash_value
        elif data['transaction_type'] == 'withdrawal':
            asset_dict['cash'] -= total_cash_value
        elif data['transaction_type'] == 'buy':
            asset_dict[data['asset_category']] += total_transaction_value
        elif data['transaction_type'] == 'sell':
            asset_dict[data['asset_category']] -= total_transaction_value

    # 음수 값을 0으로 설정하고 총합 계산
    asset_dict = {key: max(0, value) for key, value in asset_dict.items()}
    total_value = sum(asset_dict.values())

    # 전체 자산 비율 계산
    if total_value > 0:
        asset_dict = {key: round((value / total_value) * 100, 2) for key, value in asset_dict.items()}
    else:
        asset_dict = {key: 0 for key in asset_dict}

    return asset_dict

def calculate_asset_sum_by_name():
    all_data = Transaction.objects.all().values()
    asset_dict = {}

    for data in all_data:
        total_transaction_value = data['transaction_amount'] * data['quantity']
        total_cash_value = data["transaction_amount"]  # quantity of deposit and withdrawal is always 0

        # deposit과 withdrawal의 경우 asset_name이 없으므로 cash에만 반영
        if data['transaction_type'] == 'deposit':
            asset_dict['cash'] = asset_dict.get('cash', 0) + total_cash_value
        elif data['transaction_type'] == 'withdrawal':
            asset_dict['cash'] = asset_dict.get('cash', 0) - total_cash_value
        else:
            # buy와 sell의 경우 asset_name을 기반으로 자산 관리
            asset_name = data['asset_name']
            
            # 자산 이름이 asset_dict에 없으면 0으로 초기화
            if asset_name not in asset_dict:
                asset_dict[asset_name] = 0

            if data['transaction_type'] == 'buy':
                asset_dict[asset_name] += total_transaction_value
            elif data['transaction_type'] == 'sell':
                asset_dict[asset_name] -= total_transaction_value

    # 음수 값을 0으로 설정하고 총합 계산
    asset_dict = {key: max(0, value) for key, value in asset_dict.items()}
    total_value = sum(asset_dict.values())

    # 전체 자산 비율 계산
    if total_value > 0:
        asset_dict = {key: round((value / total_value) * 100, 2) for key, value in asset_dict.items()}
    else:
        asset_dict = {key: 0 for key in asset_dict}

    return asset_dict

