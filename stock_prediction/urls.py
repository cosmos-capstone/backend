from django.urls import path
from . import views

urlpatterns = [
    path('<str:symbol>', views.StockPrediction.as_view())
]