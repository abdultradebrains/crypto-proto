import asyncio
import websockets
import json
from datetime import datetime
import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def push_snapshot(chain_data):
    # Assume chain_data includes "symbol" and "expiry_date"
    if isinstance(chain_data, dict):
        key = f"opt_chain:{chain_data['symbol']}"
        pipe = r.pipeline()
        data=json.dumps(chain_data)
        pipe.set(key, data)
        pipe.publish(key, data)
        pipe.execute()

# In your message receiver/loop, call `push_snapshot(data)`
class DeltaOptionsWebSocketClient:
    def __init__(self, symbols, result_queue):
        self.ws_url = "wss://socket.delta.exchange"  # Use correct URL from docs
        self.symbol = symbols # ['call_options', 'put_options']  
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
                    push_snapshot(data)
                    # Forward full data, filter in main app
                    self.result_queue.put(data)
                except Exception as e:
                    print(f"[{datetime.now()}] Error: {e}")
                    await asyncio.sleep(2)  # Basic backoff

# Entrypoint function to launch the socket (for threading/multiprocessing)
def run_ws(symbol, queue):
    client = DeltaOptionsWebSocketClient(symbol, queue)
    asyncio.run(client.run())