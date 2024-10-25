from django.urls import path
from . import views

urlpatterns = [
    path('stock', views.Stock.as_view(), name='stock'),
]
