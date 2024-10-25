from django.http import JsonResponse

# Create your views here.


def stock(request):
    return JsonResponse({"message": "success"})
