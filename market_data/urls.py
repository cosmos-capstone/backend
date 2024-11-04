from django.urls import path
from . import views

urlpatterns = [
    path('stock/<str:symbol>/prices', views.Stock.as_view(), name='stock_prices'),
    path('korean_stocks', views.korean_stocks, name='korean_stocks'),
    path('american_stocks', views.american_stocks, name='american_stocks'),
]
