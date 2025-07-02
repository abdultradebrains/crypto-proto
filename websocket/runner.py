import threading
import asyncio
import queue
from delta_ws_client import run_ws

# Thread-safe queue for communication
result_queue = queue.Queue()

# Parameters
symbol = ['call_options','put_options']     # Example
expiry_date = "2025-07-02"  # Example

# Launch the WebSocket listener in a background thread
ws_thread = threading.Thread(target=run_ws, args=(symbol, expiry_date, result_queue), daemon=True)
ws_thread.start()

print("WebSocket client running. Streaming messages to result_queue...")

# Minimal demonstration: print new messages as they arrive
def main_poll_loop():
    try:
        while True:
            data = result_queue.get()
            print("Received new message of size", len(str(data)))
            # Data is NOT modified here; actual filtering/processing happens in consumer, e.g., Streamlit
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main_poll_loop()