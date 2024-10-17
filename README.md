# Guide
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
python manage.py runserver
```
And check here: http://127.0.0.1:8000/dumpdata1
