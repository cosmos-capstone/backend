from django.urls import path
from . import views

urlpatterns = [
    path('dumpdata', views.dumpdata, name='dumpdata'),
]