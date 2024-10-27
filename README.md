# Guide
If you want to run this project locally, follow below instructions.  
But you don't need to install locally. Check the Links chapter.
## Install
```sh
git clone git@github.com:cosmos-capstone/backend.git cosmos-backend
cd cosmos-backend

python3 -m venv ./venv
source venv/bin/activate

pip3 install -r requirements.txt

python manage.py migrate
```
## Run
```sh
source venv/bin/activate
DJANGO_DEBUG_MODE=True python manage.py runserver
```
And check here: http://127.0.0.1:8000/transaction/dumpdata1

# Links
## Dump data
- http://cosmos-backend.cho0h5.org/transaction/dumpdata1
## Market data
- http://cosmos-backend.cho0h5.org/market_data/stock/AAPL/prices (American stock)
- http://cosmos-backend.cho0h5.org/market_data/stock/SPY/prices (American ETF)
- http://cosmos-backend.cho0h5.org/market_data/stock/005930.KS/prices (Korean stock)
- http://cosmos-backend.cho0h5.org/market_data/stock/117680.KS/prices (Korean ETF)
## API Document
- http://cosmos-backend.cho0h5.org/api/schema/swagger/
