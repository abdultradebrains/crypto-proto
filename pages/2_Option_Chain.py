from collections import defaultdict
import streamlit as st
from utils import fetch_option_chain, process_raw_options_data
import pandas as pd
if 'options_data_by_strike' not in st.session_state:
    st.session_state.options_data_by_strike = defaultdict(lambda: {"call_data": {}, "put_data": {}})

st.set_page_config(
    page_title="Option Chain",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)
st.title("Option Chain data")

df = fetch_option_chain()
debug_df = df.copy()
df= df[['greeks.delta', 'greeks.gamma', 'greeks.vega', 'greeks.theta', 'greeks.rho','oi',
        'oi_change_usd_6h','open', 'high', 'low', 'close', 'volume',
        'strike_price',  'contract_type','symbol']]
process_raw_options_data(df)


def display_options_data():
    st.title("Real-time Options Chain")
    # Create a list of dictionaries for display in Streamlit table
    display_data = []
    for strike, data in st.session_state.options_data_by_strike.items():
        call = data["call_data"]
        put = data["put_data"]
        display_data.append({
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
            "Put Rho": put.get("greeks.rho"),
            # "Combined Delta": data.get("combined_delta") # Example of a calculated field
        })
    if display_data:
        st.dataframe(pd.DataFrame(display_data))
    else:
        st.write("No options data available yet.")
display_options_data()
with st.expander("Debug Info", expanded=False):
    st.write(f"Symbol: BTC")
    st.dataframe(debug_df)
