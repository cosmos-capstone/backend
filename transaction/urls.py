from django.urls import path
from . import views

urlpatterns = [
    path('dumpdata1', views.dumpdata1, name='dumpdata1'),
    path('submit', views.submit, name='submit'),
]
