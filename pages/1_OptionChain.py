import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Option Chain Visualization", layout="wide")
st.title("Option Chain Visualization")

@st.cache_data(ttl=3600)
def fetch_option_chain():
    url = "https://api.india.delta.exchange/v2/products?contract_types=call_options,put_options&states=expired,live,upcoming"
    r = requests.get(url)
    if r.ok:
        api_data = r.json()
        products = api_data.get("result", [])
        df = pd.json_normalize(products)
        df = df[[
            "id", "symbol", "strike_price", "contract_type", "state",
            "description", "maker_commission_rate", "taker_commission_rate",
            "short_description"
        ]]
        return df
    else:
        st.error("Failed to fetch data from Delta Exchange API.")
        return pd.DataFrame()

def show_option_chain(df):
    for idx, row in df.iterrows():
        symbol = row["symbol"]
        st.markdown(f"- [{symbol}](./Candlestick_Chart?symbol={symbol})")

# Fetch and cache API data (refreshes every 1 hour)
df = fetch_option_chain()

if not df.empty:
    # Unique values for filters
    all_symbols = sorted(df["symbol"].unique())
    all_contract_types = sorted(df["contract_type"].unique())
    all_strikes = sorted(df["strike_price"].unique())

    # Sidebar filters
    st.sidebar.header("Filter Options")

    search_text = st.sidebar.text_input("Search Symbol", "")
    # selected_symbols = st.sidebar.multiselect("Select Symbol(s)", all_symbols, default=all_symbols)
    selected_types = st.sidebar.multiselect("Contract Type", all_contract_types, default=all_contract_types)
    selected_strikes = st.sidebar.multiselect("Strike Price", all_strikes, default=all_strikes)

    # Apply filters on DataFrame
    filtered_df = df[
        # df["symbol"].isin(selected_symbols) &
        df["contract_type"].isin(selected_types) &
        df["strike_price"].isin(selected_strikes)
    ]

    if search_text:
        filtered_df = filtered_df[filtered_df["symbol"].str.contains(search_text, case=False)]

    st.subheader(f"Filtered Options: {len(filtered_df)} results")
    show_option_chain(filtered_df)
else:
    st.warning("No data to display.")
