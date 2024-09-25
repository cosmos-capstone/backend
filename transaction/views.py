from django.http import JsonResponse

def dumpdata(request):
    return JsonResponse({'message': 'Hello, World!'})