from django.urls import path
from . import views

urlpatterns = [
    path('test', views.TransactionView.as_view(), name='test'),
    path('portfolio', views.PortfolioView.as_view(), name='portfolio'),
    path('portfolio_sum', views.PortfolioTotalView.as_view(), name='portfolio_sum'),
    path('rebalancing', views.RebalancingView.as_view(), name='rebalancing'),
    path('asset', views.AssetView.as_view(), name='asset'),
]