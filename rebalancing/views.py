from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from transaction.models import Transaction



# Create your views here.
class RebalancingView(APIView):
    def get(self, request, *args, **kwargs):
                    return list(Transaction.objects.all().values())