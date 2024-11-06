from django.urls import path
from . import views

urlpatterns = [
    path('rebalancing', views.RebalancingView.as_view())
]
