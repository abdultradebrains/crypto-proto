import asyncio
import websockets
import json
from datetime import datetime

class DeltaOptionsWebSocketClient:
    def __init__(self, symbols, expiry_date, result_queue):
        self.ws_url = "wss://socket.delta.exchange"  # Use correct URL from docs
        self.symbol = symbols # ['call_options', 'put_options']  
        self.expiry_date = expiry_date  # e.g., "2024-07-05"
        self.result_queue = result_queue

    async def subscribe(self, ws):
        subscription_msg = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "v2/ticker",
                        "symbols": self.symbol
                    }
                ]
            }
        }
        await ws.send(json.dumps(subscription_msg))

    async def run(self):
        async with websockets.connect(self.ws_url) as ws:
            await self.subscribe(ws)
            while True:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    # print(data)
                    # Forward full data, filter in main app
                    self.result_queue.put(data)
                except Exception as e:
                    print(f"[{datetime.now()}] Error: {e}")
                    await asyncio.sleep(2)  # Basic backoff

# Entrypoint function to launch the socket (for threading/multiprocessing)
def run_ws(symbol, expiry_date, queue):
    client = DeltaOptionsWebSocketClient(symbol, expiry_date, queue)
    asyncio.run(client.run())