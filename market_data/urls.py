from django.urls import path
from . import views

urlpatterns = [
    path('stock/<str:symbol>/prices', views.Stock.as_view(), name='stock_prices'),
    path('stocks', views.stocks, name='stocks'),
]
