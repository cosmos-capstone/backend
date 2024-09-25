from django.http import JsonResponse
from django.core import serializers
from .models import Transaction

def dumpdata(request):
    return JsonResponse({'message': 'success', 'data': list(Transaction.objects.values())})