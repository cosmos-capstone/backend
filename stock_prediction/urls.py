from django.urls import path
from . import views

urlpatterns = [
    path('stock/<str:symbol>/prediction', views.StockPrediction.as_view(), name='stock_prediction')
]