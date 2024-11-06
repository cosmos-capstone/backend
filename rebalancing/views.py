from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from transaction.models import Transaction


print(Transaction.objects.all().values())

# Create your views here.
class RebalancingView(APIView):
    def get(self, request, *args, **kwargs):
                    return JsonResponse({
                    "message": "success",
                    "data": list(Transaction.objects.all().values())
                }, safe=False)