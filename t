[1mdiff --git a/market_data/urls.py b/market_data/urls.py[m
[1mindex 80fbaa0..4fda228 100644[m
[1m--- a/market_data/urls.py[m
[1m+++ b/market_data/urls.py[m
[36m@@ -2,5 +2,5 @@[m [mfrom django.urls import path[m
 from . import views[m
 [m
 urlpatterns = [[m
[31m-    path('stock', views.Stock.as_view(), name='stock'),[m
[32m+[m[32m    path('stock/<str:symbol>/prices', views.Stock.as_view(), name='stock_prices'),[m
 ][m
[1mdiff --git a/market_data/views.py b/market_data/views.py[m
[1mindex 9f02904..08f1644 100644[m
[1m--- a/market_data/views.py[m
[1m+++ b/market_data/views.py[m
[36m@@ -12,13 +12,13 @@[m [mclass Stock(APIView):[m
             OpenApiParameter([m
                 name="symbol",[m
                 type=str,[m
[31m-                location=OpenApiParameter.QUERY,[m
[32m+[m[32m                location=OpenApiParameter.PATH,[m
                 required=True,[m
                 description="The stock symbol for which to retrieve prices (e.g., 'AAPL' for Apple Inc. and '005930.KS' for Samsung Electorinics)"[m
             )[m
         ],[m
     )[m
     def get(self, request, *args, **kwargs):[m
[31m-        symbol = request.GET.get('symbol')[m
[32m+[m[32m        symbol = kwargs.get('symbol')[m
         name, currency, data = StockPrice.get_stock_prices(symbol)[m
         return JsonResponse({"name": name, "currency": currency, "data": data})[m
