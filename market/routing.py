from django.urls import re_path
from .consumers import StockPriceConsumer

websocket_urlpatterns = [
    re_path(r'ws/prices/$', StockPriceConsumer.as_asgi()),
]