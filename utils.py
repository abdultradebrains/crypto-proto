import pandas as pd
import json
import streamlit.components.v1 as components
from datetime import datetime
import streamlit as st
import requests
@st.cache_data(ttl=3600)
def fetch_option_chain_list():
    url = "https://api.india.delta.exchange/v2/products?contract_types=call_options,put_options&states=expired,live,upcoming"
    r = requests.get(url)
    if r.ok:
        api_data = r.json()
        products = api_data.get("result", [])
        df = pd.json_normalize(products)
        df = df[[
            "id", "symbol", "strike_price", "contract_type", "state",
            "description", "maker_commission_rate", "taker_commission_rate",
            "short_description","underlying_asset.symbol",'launch_time'
        ]]
        return df
    else:
        st.error("Failed to fetch data from Delta Exchange API.")
        return pd.DataFrame()
    
def fetch_option_chain(asset="BTC",date="02-07-2025"):
    url=f"https://api.india.delta.exchange/v2/tickers?contract_types=call_options,put_options&underlying_asset_symbols={asset}&expiry_date={date}"
    r = requests.get(url)
    if r.ok:
        api_data = r.json()
        tickers = api_data.get("result", [])
        df = pd.json_normalize(tickers)
        df = df.drop(columns=['initial_margin','tags','tick_size','turnover','turnover_symbol',])
        # df['time'] = pd.to_datetime(df['expiry_date'])
        return df
    else:
        st.error("Failed to fetch data from Delta Exchange API.")
        return pd.DataFrame()
    
def render_graph(df,interval):
    # --- Process Data ---
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time')
    df['time'] = df['time'].astype(int)  # UNIX timestamp
    df['time'] = df['time'] + 19800
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


def process_raw_options_data(df: pd.DataFrame):
    """
    Processes the raw DataFrame to merge call and put options by strike price.

    """
    for index, row in df.iterrows():
        strike_price = row['strike_price']
        contract_type = row['contract_type']
        if contract_type == 'call_options':
            st.session_state.options_data_by_strike[strike_price]["call_data"] = row.to_dict()
        elif contract_type == 'put_options':
            st.session_state.options_data_by_strike[strike_price]["put_data"] = row.to_dict()
        # print(st.session_state.options_data_by_strike)

    # You can add calculations here as well
    # for strike, data in st.session_state.options_data_by_strike.items():
    #     call_greeks_delta = data["call_data"].get("greeks_delta", 0)
    #     put_greeks_delta = data["put_data"].get("greeks_delta", 0)
    #     # Example calculation: sum of deltas
    #     data["combined_delta"] = call_greeks_delta + put_greeks_delta
    # return data