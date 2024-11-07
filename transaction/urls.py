from django.urls import path
from . import views

urlpatterns = [
    path('dumpdata1', views.dumpdata1, name='dumpdata1'),
    path('test', views.TransactionView.as_view(), name='test'),
    path('myaccount', views.TransactionView.as_view(), name='test'),
    path('rebalancing', views.TransactionView.as_view(), name='rebalancing'),
]
