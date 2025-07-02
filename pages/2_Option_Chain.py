import streamlit as st
from utils import fetch_option_chain


st.set_page_config(
    page_title="Option Chain",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)
st.title("Option Chain data")

df = fetch_option_chain()
df= df[['greeks.delta', 'greeks.gamma', 'greeks.vega', 'greeks.theta', 'greeks.rho','oi',
        'oi_change_usd_6h','open', 'high', 'low', 'close', 'volume',
        'strike_price',  'contract_type','symbol']]
df_grouped = df.groupby('strike_price')


def show_option_chain(df):
    for strike_price, group in df_grouped:
        st.subheader(f"Strike Price: {strike_price}")
        st.dataframe(group)
show_option_chain(df_grouped)
with st.expander("Debug Info", expanded=False):
    st.write(f"Symbol: BTC")
    st.dataframe(df)
