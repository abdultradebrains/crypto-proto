# api_gateway/main.py
import asyncio
import json
import os
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# The application instance
app = FastAPI()

# Connection manager to keep track of active clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def redis_listener(manager: ConnectionManager):
    """Listens to Redis Pub/Sub and broadcasts messages to all connected clients."""
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
    async with r.pubsub() as pubsub:
        await pubsub.psubscribe("opt_chain:*")
        print("API Gateway started listening to Redis channel 'opt_chain:*'")
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    # Forward the exact data payload to the frontend
                    await manager.broadcast(message["data"])
            except Exception as e:
                print(f"Error in Redis listener: {e}")
                await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    """On startup, run the redis_listener as a background task."""
    asyncio.create_task(redis_listener(manager))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """The main WebSocket endpoint for frontend clients."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)