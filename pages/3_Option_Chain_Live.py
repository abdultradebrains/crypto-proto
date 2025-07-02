# streamlit/streamlit_app.py
import streamlit as st
import pandas as pd
import redis
import json
import os
import queue
import threading
import time
from collections import defaultdict, deque

# --- Global Queue & Redis Subscriber (Unchanged - This part is working correctly) ---
GLOBAL_DATA_QUEUE = queue.Queue()

class RedisSubscriber(threading.Thread):
    # ... (The RedisSubscriber class code remains exactly the same as the previous version)
    def __init__(self, data_queue: queue.Queue):
        super().__init__(daemon=True)
        self.data_queue = data_queue
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)), decode_responses=True)
        self.pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)
        self._running = True
        self.is_connected = False
    def run(self):
        try:
            self.redis_client.ping()
            self.is_connected = True
            self.pubsub.psubscribe("opt_chain:*")
            for message in self.pubsub.listen():
                if not self._running: break
                try:
                    data = json.loads(message["data"])
                    self.data_queue.put(data)
                except (json.JSONDecodeError, KeyError): pass
        except redis.exceptions.ConnectionError: self.is_connected = False
    def stop(self):
        self._running = False
        if self.pubsub: self.pubsub.close()

# --- Main Application ---
def main():
    # --- Session State Initialization ---
    if 'subscriber_thread' not in st.session_state:
        st.session_state.subscriber_thread = RedisSubscriber(GLOBAL_DATA_QUEUE)
        st.session_state.subscriber_thread.start()
        st.session_state.data_queue = GLOBAL_DATA_QUEUE
        st.session_state.chain_by_strike = defaultdict(dict)
        st.session_state.dynamic_filters = {"assets": set(), "expiries": set()}
        # Add a deque for our live log
        st.session_state.log = deque(maxlen=20)
        print("Initialized Streamlit session and started Redis subscriber.")

    # --- Data Processing Function (with logging) ---
    def process_queue_and_update_state():
        q = st.session_state.data_queue
        while not q.empty():
            try:
                data = q.get_nowait()
                instrument = data.get("instrument_name", "")
                parts = instrument.split('-')
                
                if len(parts) < 4:
                    st.session_state.log.appendleft(f"⚠️ REJECTED (bad name): {instrument}")
                    continue
                
                contract_type_char, asset, strike_str, expiry = parts
                strike = int(strike_str)
                
                # Update state
                st.session_state.dynamic_filters["assets"].add(asset)
                st.session_state.dynamic_filters["expiries"].add(expiry)
                side = "call" if contract_type_char == "C" else "put"
                st.session_state.chain_by_strike[strike][side] = data
                st.session_state.log.appendleft(f"✅ PROCESSED: {instrument}")

            except queue.Empty:
                break
            except (ValueError, IndexError, KeyError) as e:
                st.session_state.log.appendleft(f"❌ ERROR processing: {data}. Reason: {e}")

    # --- UI and Table Rendering Functions (Unchanged) ---
    def render_ui_and_get_filters():
        st.set_page_config(page_title="Real-Time Options Chain", layout="wide")
        st.title("⚡ Real-Time Options Chain")
        asset_options = ["All"] + sorted(list(st.session_state.dynamic_filters["assets"]))
        expiry_options = ["All"] + sorted(list(st.session_state.dynamic_filters["expiries"]))
        col1, col2 = st.columns(2)
        with col1: asset_filter = st.selectbox("Filter by Asset", options=asset_options)
        with col2: expiry_filter = st.selectbox("Filter by Expiry", options=expiry_options)
        return asset_filter, expiry_filter

    def render_table_in_placeholder(asset_filter, expiry_filter, placeholder):
        # (This function is exactly the same as the previous version)
        rows = []
        sorted_strikes = sorted(st.session_state.chain_by_strike.items())
        for strike, data in sorted_strikes:
            call, put = data.get("call", {}), data.get("put", {})
            asset, expiry = call.get("symbol") or put.get("symbol"), call.get("expiry_date") or put.get("expiry_date")
            if (asset_filter == "All" or asset == asset_filter) and (expiry_filter == "All" or expiry == expiry_filter):
                rows.append({
                    "Call Delta": call.get("greeks", {}).get("delta"), "Call Gamma": call.get("greeks", {}).get("gamma"), "Call Vega": call.get("greeks", {}).get("vega"), "Call Theta": call.get("greeks", {}).get("theta"), "Call Price": call.get("last_price"), "Call OI": call.get("open_interest"),
                    "STRIKE": strike,
                    "Put OI": put.get("open_interest"), "Put Price": put.get("last_price"), "Put Delta": put.get("greeks", {}).get("delta"), "Put Gamma": put.get("greeks", {}).get("gamma"), "Put Vega": put.get("greeks", {}).get("vega"), "Put Theta": put.get("greeks", {}).get("theta"),
                })
        with placeholder.container():
            if rows:
                df = pd.DataFrame(rows, columns=[
                    "Call Delta", "Call Gamma", "Call Vega", "Call Theta", "Call Price", "Call OI", "STRIKE",
                    "Put OI", "Put Price", "Put Delta", "Put Gamma", "Put Vega", "Put Theta"
                ]).set_index("STRIKE")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data available for the selected filters. Waiting for updates...")

    # --- ENHANCED DEBUG SECTION ---
    def render_debug_section():
        with st.expander("Show Live Data Flow & Debug Information"):
            st.subheader("Pipeline Status")
            subscriber = st.session_state.subscriber_thread
            col1, col2, col3 = st.columns(3)
            col1.metric("Redis Connection", "✅ Connected" if subscriber.is_connected else "❌ Disconnected")
            col2.metric("Subscriber Thread", "✅ Running" if subscriber.is_alive() else "❌ Stopped")
            col3.metric("Items in Queue", st.session_state.data_queue.qsize())
            st.divider()

            st.subheader("Live Processing Log (Last 20 Items)")
            st.code("\n".join(st.session_state.log))
            st.divider()

            st.subheader("Unfiltered Data State")
            st.metric("Total Strikes in State", len(st.session_state.chain_by_strike))
            st.write("Current data stored in `st.session_state.chain_by_strike`:")
            st.json(st.session_state.chain_by_strike, expanded=False)


    # --- Main Application Loop ---
    process_queue_and_update_state()
    asset_f, expiry_f = render_ui_and_get_filters()
    
    # The debug section is now separate from the main placeholder
    render_debug_section() 
    
    table_placeholder = st.empty()

    while True:
        process_queue_and_update_state()
        render_table_in_placeholder(asset_f, expiry_f, table_placeholder)
        time.sleep(0.1)

if __name__ == "__main__":
    main()