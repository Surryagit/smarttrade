from rest_framework import generics, permissions
from .models import Stock
from .serializers import StockSerializer

class StockListCreateView(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Stock.objects.filter(user=self.request.user)


class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Stock.objects.filter(user=self.request.user)