import json
import asyncio
import yfinance as yf
from channels.generic.websocket import AsyncWebsocketConsumer

class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        # Start sending prices every 10 seconds
        asyncio.create_task(self.send_prices())

    async def disconnect(self, close_code):
        self.running = False

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.symbols = data.get('symbols', [])

    async def send_prices(self):
        while self.running:
            try:
                if hasattr(self, 'symbols') and self.symbols:
                    prices = {}
                    for symbol in self.symbols:
                        ticker = yf.Ticker(symbol)
                        price = ticker.info.get('currentPrice',
                                ticker.info.get('regularMarketPrice', 0))
                        prices[symbol] = price

                    await self.send(text_data=json.dumps({
                        'type': 'price_update',
                        'prices': prices
                    }))
            except Exception as e:
                pass
            await asyncio.sleep(10)