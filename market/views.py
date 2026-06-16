import yfinance as yf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class StockPriceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, symbol):
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            data = {
                'symbol': symbol.upper(),
                'name': info.get('longName', 'N/A'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'previous_close': info.get('previousClose', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD'),
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class PortfolioPriceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from portfolio.models import Stock
        stocks = Stock.objects.filter(user=request.user)
        
        result = []
        total_invested = 0
        total_current = 0

        for stock in stocks:
            try:
                ticker = yf.Ticker(stock.symbol)
                current_price = ticker.info.get('currentPrice', ticker.info.get('regularMarketPrice', 0))
                invested = float(stock.quantity) * float(stock.buy_price)
                current_value = float(stock.quantity) * current_price
                profit_loss = current_value - invested
                profit_loss_pct = (profit_loss / invested * 100) if invested > 0 else 0

                total_invested += invested
                total_current += current_value

                result.append({
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'quantity': float(stock.quantity),
                    'buy_price': float(stock.buy_price),
                    'current_price': current_price,
                    'invested': round(invested, 2),
                    'current_value': round(current_value, 2),
                    'profit_loss': round(profit_loss, 2),
                    'profit_loss_pct': round(profit_loss_pct, 2),
                })
            except:
                result.append({
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'error': 'Could not fetch price'
                })

        return Response({
            'stocks': result,
            'total_invested': round(total_invested, 2),
            'total_current_value': round(total_current, 2),
            'total_profit_loss': round(total_current - total_invested, 2),
            'total_profit_loss_pct': round((total_current - total_invested) / total_invested * 100, 2) if total_invested > 0 else 0,
        })