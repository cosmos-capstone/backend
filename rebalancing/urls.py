from django.urls import path
from . import views

urlpatterns = [
    path('', views.RebalancingView.as_view())
]
