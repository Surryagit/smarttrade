from django.urls import path
from .views import StockListCreateView, StockDetailView

urlpatterns = [
    path('', StockListCreateView.as_view(), name='stock-list'),
    path('<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
]