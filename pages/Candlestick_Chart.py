import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import json
from streamlit_autorefresh import st_autorefresh
from utils import render_graph, fetch_option_chain
st_autorefresh(interval=300000, key="refresh")  # every 5 minutes

# --- Setup ---
st.set_page_config(layout="wide")
symbol = st.query_params.get('symbol', None)
df = fetch_option_chain()
all_symbols = sorted(df["symbol"].unique())
col1, col2 = st.columns(2)
with col1:
    symbol = st.selectbox("Select Symbol", all_symbols, index = 0 if symbol is None else all_symbols.index(symbol))
with col2:
    type = st.selectbox("Select Type", ["Trade", "Mark"], index=1)
symbol= "MARK:"+symbol if type == "Mark" else symbol
st.write(f"## Candlestick for {symbol}")

# --- Interval Selection ---
duration_mapping = {
    "5 Minute": "5m", "15 Minute": "15m", "1 Hour": "1h"
}
duration_label = st.selectbox("Select Duration", list(duration_mapping.keys()))
interval = duration_mapping[duration_label]

# --- Fetch Candle Data ---
current_ts = int(datetime.now().timestamp())
url = f"https://api.india.delta.exchange/v2/history/candles?resolution={interval}&symbol={symbol}&start=1719300782&end={current_ts}"
response = requests.get(url)

ohlc = response.json()["result"]
df = pd.DataFrame(ohlc)
debug_data = df.copy()
try:
    render_graph(df, interval)
except Exception as e:
    # st.error(f"Error rendering graph: {e}")
    st.error("Please check the symbol, Maybe it doesnt have data for this duration or try again.")
    st.stop()

with st.expander("Debug Info", expanded=False):
    st.write(f"Symbol: {symbol}")
    st.write(f"Interval: {interval}")
    st.write(f"Data Points: {len(df)}")
    debug_data['time'] = pd.to_datetime(debug_data['time'], unit='s', utc=True)
    debug_data['time'] = debug_data['time'].dt.tz_convert('Asia/Kolkata')
    debug_data['time'] = debug_data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    st.dataframe(debug_data)  # Display the data in JSON format for debugging