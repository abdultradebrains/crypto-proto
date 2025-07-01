import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import json
from streamlit_autorefresh import st_autorefresh
from utils import render_graph
st_autorefresh(interval=300000, key="refresh")  # every 5 minutes

# --- Setup ---
st.set_page_config(layout="wide")
symbol = st.query_params.get('symbol', ['BTCUSDT'])
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
try:
    render_graph(df, interval)
except Exception as e:
    # st.error(f"Error rendering graph: {e}")
    st.error("Please check the symbol, Maybe it doesnt have data for this duration or try again.")
    st.stop()