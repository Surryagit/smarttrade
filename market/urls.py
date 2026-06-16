from django.urls import path
from .views import StockPriceView, PortfolioPriceView

urlpatterns = [
    path('price/<str:symbol>/', StockPriceView.as_view(), name='stock-price'),
    path('portfolio-value/', PortfolioPriceView.as_view(), name='portfolio-value'),
]