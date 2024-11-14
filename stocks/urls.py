# stocks/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page with buttons
    path('get_image/<str:company>/<str:graph_type>/', views.get_image_url, name='get_image_url'),
    path('get_live_prices/', views.get_live_prices, name='get_live_prices'),
    path('stocks/movers/', views.display_stock_movers, name='STOCKS'),
]