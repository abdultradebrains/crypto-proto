import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import json

# --- Setup ---
st.set_page_config(layout="wide")
symbol = st.experimental_get_query_params().get('symbol', ['BTCUSDT'])[0]
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

# --- Process Data ---
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values('time')
df['time'] = df['time'].astype(int)  # UNIX timestamp

# Ensure numeric data
for col in ['open', 'high', 'low', 'close']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Convert to JS-friendly data format ---
candles = df[['time', 'open', 'high', 'low', 'close']].to_dict(orient='records')
js_data = json.dumps(candles)
seconds_visible = "true" if interval in ["1m", "3m", "5m", "15m"] else "false"
# --- Streamlit Debug View ---

components.html(f"""
<div id="container" style="width: 100%; height: 500px;"></div>
<script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
<script>
    const chart = LightweightCharts.createChart(document.getElementById('container'), {{
        layout: {{
            background: {{ type: 'solid', color: 'white' }},
            textColor: 'black'
        }},
        width: window.innerWidth * 0.9,
        height: 500,
        timeScale: {{
            timeVisible: true,
            secondsVisible: {seconds_visible}
        }}
    }});

    const candlestickSeries = chart.addSeries(LightweightCharts.CandlestickSeries,{{
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350'
    }});

    candlestickSeries.setData({js_data});
    chart.timeScale().fitContent();
    

    
</script>
""", height=550)