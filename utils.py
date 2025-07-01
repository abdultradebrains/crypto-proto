import pandas as pd
import json
import streamlit.components.v1 as components
from datetime import datetime

def render_graph(df,interval):
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