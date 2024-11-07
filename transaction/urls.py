from django.urls import path
from . import views

urlpatterns = [
    path('dumpdata1', views.dumpdata1, name='dumpdata1'),
    path('test', views.TransactionView.as_view(), name='test'),
    path('portfolio', views.PortfolioView.as_view(), name='portfolio'),
    path('rebalancing', views.RebalancingView.as_view(), name='rebalancing'),
]
