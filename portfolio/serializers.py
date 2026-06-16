from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    total_invested = serializers.ReadOnlyField()

    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'quantity', 'buy_price', 'total_invested', 'date_added']
        read_only_fields = ['date_added']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)