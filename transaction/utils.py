# utils.py
from .models import Transaction
import yfinance as yf
from decimal import Decimal
from datetime import datetime, timedelta

def rebalance_asset(portfolio):
    # sharp ratio of stock 3-Q : K=-0.07, A=1.99,   
    # sharp ratio of bond 3-Q : K=0.79, A=0.05,
    
    # K/A deposit interest rate
    risk_free_rate = 0.022
    # end_date = datetime.today()
    # start_date = end_date - timedelta(days=365)
    
    # kospi = fdr.DataReader('KS11', start_date, end_date)  # KOSPI
    # nasdaq = fdr.DataReader('IXIC', start_date, end_date)  # NASDAQ

    # kospi_1y_return = (kospi['Close'][-1] / kospi['Close'][0]) - 1
    # nasdaq_1y_return = (nasdaq['Close'][-1] / nasdaq['Close'][0]) - 1
    # num_days = len(kospi['Close'].dropna())

    # kospi_std_dev = kospi['Close'].pct_change().std() * np.sqrt(num_days)
    # nasdaq_std_dev = nasdaq['Close'].pct_change().std() * np.sqrt(num_days)

    sharpe_ratios = {
        # 'korean_stock': (kospi_1y_return - risk_free_rate) / kospi_std_dev,
        # 'american_stock': (nasdaq_1y_return - risk_free_rate) / nasdaq_std_dev,
        'korean_stock': 0.7,
        'american_stock': 0.9,
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
        asset: round(Decimal(str(portfolio.get(asset, 0))) * weight_current + 
                Decimal(str(target_portfolio.get(asset, 0))) * weight_target, 2)
        for asset in set(portfolio) | set(target_portfolio)
    }
    return final_portfolio


def calculate_asset_sum(date):
    all_data = Transaction.objects.filter(transaction_date__lte=date).values()
    asset_dict = {
        'korean_stock': 0.0,
        'american_stock': 0.0,
        'korean_bond': 0.0,
        'american_bond': 0.0,
        'fund': 0.0,
        'commodity': 0.0,
        'gold': 0.0,
        'deposit': 0.0,
        'cash': 0.0,
    }
    
    for data in all_data:
        total_cash_value = data["transaction_amount"]  # quantity of deposit and withdrawal is always 0
        total_transaction_value = float(data['transaction_amount'])
        
        # 가장 최근 주가 가져오기 (종가)
        ticker = data["asset_symbol"]
        try:
            recent_data = yf.download(ticker, period="1d")
            latest_close = float(recent_data['Close'].iloc[-1].item())

            stock = yf.Ticker(ticker)
            currency = stock.info.get("currency", "Unknown")
            if currency == "USD":
                total_transaction_value = float(data['quantity']) * latest_close * 1400 # 산 당시 가격이 아니라 최근 가격으로 곱해서 
            else:
                total_transaction_value = float(data['quantity']) * latest_close # 산 당시 가격이 아니라 최근 가격으로 곱해서 
        except Exception as e:
            pass
        
        if data['transaction_type'] == 'deposit':
            asset_dict['cash'] += float(total_cash_value)
        elif data['transaction_type'] == 'withdrawal':
            asset_dict['cash'] -= float(total_cash_value)
        elif data['transaction_type'] == 'buy':
            asset_dict[data['asset_category']] += float(total_transaction_value)
            asset_dict['cash'] -= float(total_transaction_value)
        elif data['transaction_type'] == 'sell':
            asset_dict[data['asset_category']] -= float(total_transaction_value)
            asset_dict['cash'] += float(total_transaction_value)

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
        total_cash_value = data["transaction_amount"]  # quantity of deposit and withdrawal is always 0
        total_transaction_value = float(data['transaction_amount'])
        
        ticker = data["asset_symbol"]
        try:
            recent_data = yf.download(ticker, period="1d")
            latest_close = float(recent_data['Close'].iloc[-1].item())

            stock = yf.Ticker(ticker)
            currency = stock.info.get("currency", "Unknown")
            if currency == "USD":
                total_transaction_value = float(data['quantity']) * latest_close * 1400 # 산 당시 가격이 아니라 최근 가격으로 곱해서 
            else:
                total_transaction_value = float(data['quantity']) * latest_close # 산 당시 가격이 아니라 최근 가격으로 곱해서 
        except Exception as e:
            pass
        
        # deposit과 withdrawal의 경우 asset_name이 없으므로 cash에만 반영
        if data['transaction_type'] == 'deposit':
            asset_dict['cash'] = asset_dict.get('cash', {'rate': 0, 'sector': 'N/A', 'industry': 'N/A'})
            asset_dict['cash']['rate'] += total_cash_value
        elif data['transaction_type'] == 'withdrawal':
            asset_dict['cash'] = asset_dict.get('cash', {'rate': 0, 'sector': 'N/A', 'industry': 'N/A'})
            asset_dict['cash']['rate'] -= total_cash_value
        else:
            # buy와 sell의 경우 asset_name을 기반으로 자산 관리
            asset_name = data['asset_name']
            asset_symbol = data['asset_symbol']
            # yfinance에서 데이터 조회 및 에러 핸들링
            try:
                ticker = yf.Ticker(asset_symbol)
                info = ticker.info
                sector = info.get('sector', 'none')
                industry = info.get('industry', 'none')
            except Exception as e:
                sector = 'none'
                industry = 'none'
                print(f"Error fetching data for {asset_symbol}: {e}")

            # 자산 이름이 asset_dict에 없으면 0으로 초기화
            if asset_name not in asset_dict:
                asset_dict[asset_name] = {'rate': 0, 'sector': sector, 'industry': industry}

            if data['transaction_type'] == 'buy':
                asset_dict[asset_name]['rate'] += total_transaction_value
            elif data['transaction_type'] == 'sell':
                asset_dict[asset_name]['rate'] -= total_transaction_value

    # 음수 값을 0으로 설정하고 총합 계산
    asset_dict = {key: {'rate': max(0.0, float(value['rate'])), 'sector': value['sector'], 'industry': value['industry']}
                for key, value in asset_dict.items()}
    total_value = sum(item['rate'] for item in asset_dict.values())

    # 전체 자산 비율 계산
    if total_value > 0:
        asset_dict = {key: {'rate': round((value['rate'] / total_value) * 100, 2), 'sector': value['sector'], 'industry': value['industry']}
                      for key, value in asset_dict.items()}
    else:
        asset_dict = {key: {'rate': 0, 'sector': value['sector'], 'industry': value['industry']}
                      for key, value in asset_dict.items()}

    return asset_dict


def get_asset_totals(all_data):
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
        total_cash_value = data["transaction_amount"]  # quantity of deposit and withdrawal is always 0
        total_transaction_value = float(data['transaction_amount'])
        
        # 가장 최근 주가 가져오기 (종가)
        ticker = data["asset_symbol"]
        try:
            recent_data = yf.download(ticker, period="1d")
            latest_close = float(recent_data['Close'].iloc[-1].item())

            stock = yf.Ticker(ticker)
            currency = stock.info.get("currency", "Unknown")
            if currency == "USD":
                total_transaction_value = float(data['quantity']) * latest_close * 1400 # 산 당시 가격이 아니라 최근 가격으로 곱해서 
            else:
                total_transaction_value = float(data['quantity']) * latest_close # 산 당시 가격이 아니라 최근 가격으로 곱해서 
        except Exception as e:
            pass
        
        if data['transaction_type'] == 'deposit':
            asset_dict['cash'] += float(total_cash_value)
        elif data['transaction_type'] == 'withdrawal':
            asset_dict['cash'] -= float(total_cash_value)
        elif data['transaction_type'] == 'buy':
            asset_dict[data['asset_category']] += float(total_transaction_value)
            asset_dict['cash'] -= float(total_transaction_value)
        elif data['transaction_type'] == 'sell':
            asset_dict[data['asset_category']] -= float(total_transaction_value)
            asset_dict['cash'] += float(total_transaction_value)

    asset_dict = {key: max(0, value) for key, value in asset_dict.items()}

    return asset_dict

def get_rebalanced_transaction(rebalanced_portfolio, date):
    def add_seconds_to_date(date, seconds):
        """
        date: datetime 객체 또는 ISO 8601 문자열 (예: '2023-01-01T10:00:00Z').
        seconds: 초 단위로 추가할 시간.
        """
        if isinstance(date, str):
            # ISO 8601 문자열이라면 datetime 객체로 변환
            date = datetime.fromisoformat(date.replace("Z", "+00:00"))
        
        # 초 단위 시간 추가
        new_date = date + timedelta(seconds=seconds)
        
        # ISO 8601 형식으로 반환
        return new_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    filtered_data = Transaction.objects.filter(transaction_date__lte=date).values()
    past_portfolio = get_asset_totals(filtered_data)
    past_sum = sum(past_portfolio.values())
    for key in rebalanced_portfolio:
        rebalanced_portfolio[key] = float(rebalanced_portfolio[key]) * float(past_sum) / 100

    return [
        {
            "id": 0,
            "transaction_date": add_seconds_to_date(date, 0),
            "transaction_type": "deposit",
            "asset_category": "cash",
            "asset_symbol": "",
            "asset_name": "",
            "quantity": 0,
            "transaction_amount": str(past_sum)
        },
        {
            "id": 1,
            "transaction_date": add_seconds_to_date(date, 1),
            "transaction_type": "buy",
            "asset_category": "korean_stock",
            "asset_symbol": "102110.KS",
            "asset_name": "TIGER 200",
            "quantity": 1,
            "transaction_amount": "1000.00"
        },
        {
            "id": 2,
            "transaction_date": add_seconds_to_date(date, 2),
            "transaction_type": "buy",
            "asset_category": "korean_stock",
            "asset_symbol": "481430.KS",
            "asset_name": "RISE 국고채10년액티브",
            "quantity": 1,
            "transaction_amount": "1000.00"
        },
        {
            "id": 3,
            "transaction_date": add_seconds_to_date(date, 3),
            "transaction_type": "buy",
            "asset_category": "american_stock",
            "asset_symbol": "SPY",
            "asset_name": "SPDR S&P 500 ETF Trust",
            "quantity": 1,
            "transaction_amount": "728123.00"
        },
        {
            "id": 4,
            "transaction_date": add_seconds_to_date(date, 4),
            "transaction_type": "buy",
            "asset_category": "american_stock",
            "asset_symbol": "BND",
            "asset_name": "Vanguard Total Bond Market Index Fund",
            "quantity": 1,
            "transaction_amount": "728123.00"
        },
        {
            "id": 5,
            "transaction_date": add_seconds_to_date(date, 5),
            "transaction_type": "buy",
            "asset_category": "american_stock",
            "asset_symbol": "VTI",
            "asset_name": "Vanguard Total Stock Market Index Fund ETF Shares",
            "quantity": 1,
            "transaction_amount": "728123.00"
        },
        {
            "id": 6,
            "transaction_date": add_seconds_to_date(date, 6),
            "transaction_type": "buy",
            "asset_category": "american_stock",
            "asset_symbol": "DBC",
            "asset_name": "Invesco DB Commodity Index Tracking Fund",
            "quantity": 1,
            "transaction_amount": "728123.00"
        },
        {
            "id": 7,
            "transaction_date": add_seconds_to_date(date, 7),
            "transaction_type": "buy",
            "asset_category": "american_stock",
            "asset_symbol": "GLD",
            "asset_name": "SPDR Gold Shares",
            "quantity": 1,
            "transaction_amount": "728123.00"
        },
    ]