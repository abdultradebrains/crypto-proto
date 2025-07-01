import streamlit as st
import requests
from streamlit_lightweight_charts import renderLightweightCharts
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
url = f"https://api.india.delta.exchange/v2/history/candles?resolution={interval}&symbol={symbol}&start=1719300782&end=1751364793"
# url = f"https://api.delta.exchange/v2/candles/history?symbol={symbol}&resolution={interval}&limit=100"
response = requests.get(url)
print(url)
ohlc = response.json()["result"]
#  Suppose ohlc is a list of dicts from the API.
df = pd.DataFrame(ohlc)


# --- Assume your DataFrame is named df ---
# Required columns: 'time' (as POSIX/UNIX seconds), 'open', 'high', 'low', 'close'
# If time is not already datetime, convert:
if not pd.api.types.is_datetime64_any_dtype(df['time']):
    df['time'] = pd.to_datetime(df['time'], unit='s')

# Ensure numeric columns
for col in ['open', 'high', 'low', 'close']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Candlestick plotting ---
fig, ax = plt.subplots(figsize=(16, 6))
 # width in days for the candlestick rectangle, adjust if needed
width = 15 / 1440  # days

for idx, row in df.iterrows():
    color = 'green' if row['close'] >= row['open'] else 'red'
    # Wick
    ax.plot([row['time'], row['time']], [row['low'], row['high']], color='black', linewidth=1)
    # Candle body
    rect = plt.Rectangle(
        (mdates.date2num(row['time']) - width/2, min(row['open'], row['close'])),
        width,
        abs(row['close'] - row['open']),
        color=color
    )
    ax.add_patch(rect)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xticks(rotation=45)
ax.set_title('Candlestick Chart')
ax.set_xlabel('Time')
ax.set_ylabel('Price')
plt.tight_layout()

st.pyplot(fig)