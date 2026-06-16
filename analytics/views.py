from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from portfolio.models import Stock
from .risk_engine import calculate_risk_metrics, analyze_portfolio_risk

class StockRiskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, symbol):
        metrics = calculate_risk_metrics(symbol.upper())
        if metrics is None:
            return Response({'error': 'Could not fetch data for this symbol'}, status=400)
        return Response(metrics)


class PortfolioRiskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stocks = Stock.objects.filter(user=request.user)
        if not stocks.exists():
            return Response({'error': 'No stocks in portfolio'}, status=400)
        
        symbols = [stock.symbol for stock in stocks]
        result = analyze_portfolio_risk(symbols)
        
        if result is None:
            return Response({'error': 'Could not analyze portfolio'}, status=400)
        
        return Response(result)