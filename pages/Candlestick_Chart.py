import streamlit as st
import requests
import plotly.graph_objs as go
import pandas as pd
# Get symbol from query params (since Streamlit v1.10+ and in latest cloud versions)
symbol = st.experimental_get_query_params().get('symbol', [''])[0]
st.write(f"## Candlestick for {symbol}")

# Candlestick Duration Dropdown
duration_mapping = {
    "5 Minute": "5m", "15 Minute": "15m", "1 Hour": "1h"
}
duration_label = st.selectbox("Select Duration", list(duration_mapping.keys()))
interval = duration_mapping[duration_label]

# Fetch candlestick data from Delta Exchange API
url = f"https://api.india.delta.exchange/v2/history/candles?resolution={interval}&symbol={symbol}&start=1719300782&end=1750836782"
# url = f"https://api.delta.exchange/v2/candles/history?symbol={symbol}&resolution={interval}&limit=100"
response = requests.get(url)
print(url)
ohlc = response.json()["result"]
#  Suppose ohlc is a list of dicts from the API.
df = pd.DataFrame(ohlc)
df['time'] = pd.to_datetime(df['time'], unit='s')
for col in ['open', 'high', 'low', 'close']:
    df[col] = df[col].astype(float)
fig = go.Figure(data=[go.Candlestick(
    x=df['time'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
st.plotly_chart(fig)