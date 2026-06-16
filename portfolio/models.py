from django.db import models
from django.conf import settings

class Stock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)  # e.g. AAPL, TCS.NS
    name = models.CharField(max_length=100)   # e.g. Apple Inc.
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.symbol}"

    @property
    def total_invested(self):
        return float(self.quantity) * float(self.buy_price)