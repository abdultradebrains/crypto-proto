import streamlit as st
import pandas as pd
from websocket.runner import result_queue as queue  # Import the shared queue from the WebSocket runner
# Set up manager with your client


# Streamlit UI widgets
st.set_page_config(page_title="Crypto Option Chain", layout="wide")
st.title("Crypto Options Chain (BTC/ETH) — Real-Time")

asset = st.selectbox("Underlying Asset", ["BTC", "ETH"])
# You might want to offer valid dates dynamically depending on asset
date = st.selectbox("Expiry Date", ["2024-07-05", "2024-07-12"])  # Example dates

# Table column selector for custom display
default_fields = [
    "Call Gamma", "Call Theta", "Call Delta", "Call OI",
    "Strike Price",
    "Put OI", "Put Delta", "Put Theta", "Put Gamma",
]
# all_fields = ['close', 'contract_type', 'description', 'high', 'low', 'mark_change_24h', 'mark_price', 'mark_vol', 'oi', 'oi_change_usd_6h', 'oi_contracts', 'oi_value', 'oi_value_symbol', 'oi_value_usd', 'open', 'product_id', 'size', 'spot_price', 'strike_price', 'symbol', 'timestamp', 'turnover_usd', 'underlying_asset_symbol', 'volume', 'greeks.delta', 'greeks.gamma', 'greeks.rho', 'greeks.spot', 'greeks.theta', 'greeks.vega', 'price_band.lower_limit', 'price_band.upper_limit', 'quotes.ask_iv', 'quotes.ask_size', 'quotes.best_ask', 'quotes.best_bid', 'quotes.bid_iv', 'quotes.bid_size', 'quotes.impact_mid_price', 'quotes.mark_iv']
fields = st.multiselect("Table Columns", default_fields, default=default_fields)


# Receive and filter data in real time
if 'options_data_by_strike' not in st.session_state:
    st.session_state.options_data_by_strike = {}

def apply_incoming_data():
    """Update session state with latest websocket queue data (dict format)."""
    
    try:
        while True:  # Drain the queue
            data = queue.get_nowait()
            print(f"Received new data of size {len(str(data))}")
            # Filter and convert to DataFrame as in previous code
            df = pd.DataFrame(data['chains'])  # adapt key if needed
            df = df[df["symbol"].str.startswith(asset)]
            df = df[df["expiry_date"] == date]
            process_raw_options_data(df)  # Use your own supplied function
    except Exception as e:
        print(f"No new data in queue: {e}")  # No data to process, ignore
        pass

def process_raw_options_data(df: pd.DataFrame):
    session_dict = st.session_state.options_data_by_strike
    for index, row in df.iterrows():
        strike_price = row['strike_price']
        contract_type = row['contract_type']
        if strike_price not in session_dict:
            session_dict[strike_price] = {"call_data": {}, "put_data": {}}
        if contract_type == 'call_options':
            session_dict[strike_price]["call_data"] = row.to_dict()
        elif contract_type == 'put_options':
            session_dict[strike_price]["put_data"] = row.to_dict()

def display_options_table():
    display_data = []
    session_dict = st.session_state.options_data_by_strike
    for strike, data in session_dict.items():
        call, put = data.get("call_data", {}), data.get("put_data", {})
        row = {
            "Call Rho": call.get("greeks.rho"),
            "Call Vega": call.get("greeks.vega"),
            "Call Gamma": call.get("greeks.gamma"),
            "Call Theta": call.get("greeks.theta"),
            "Call Delta": call.get("greeks.delta"),
            "Call OI": call.get("oi"),
            "Strike Price": strike,
            "Put OI": put.get("oi"),
            "Put Delta": put.get("greeks.delta"),
            "Put Theta": put.get("greeks.theta"),
            "Put Gamma": put.get("greeks.gamma"),
            "Put Vega": put.get("greeks.vega"),
            "Put Rho": put.get("greeks.rho")
        }
        # Only add the columns selected for display
        row_filtered = {k: row[k] for k in fields if k in row}
        display_data.append(row_filtered)
    if display_data:
        st.dataframe(pd.DataFrame(display_data))
    else:
        st.write("No option chain data available yet.")

# Main app refresh loop
apply_incoming_data()
display_options_table()