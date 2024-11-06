from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from transaction.models import Transaction


print(list(Transaction.objects.all().values())[0]['asset_symbol'])

# Create your views here.
class RebalancingView(APIView):
    def get(self, request, *args, **kwargs):
                    return list(Transaction.objects.all().values())