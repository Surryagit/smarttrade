from django.urls import path
from .views import StockRiskView, PortfolioRiskView

urlpatterns = [
    path('stock/<str:symbol>/', StockRiskView.as_view(), name='stock-risk'),
    path('portfolio/', PortfolioRiskView.as_view(), name='portfolio-risk'),
]