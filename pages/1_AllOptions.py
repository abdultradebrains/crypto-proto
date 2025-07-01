import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from utils import fetch_option_chain
st.set_page_config(page_title="Option Chain Visualization", layout="wide")
st.title("Option Chain Visualization")

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
    all_spots = sorted(df["underlying_asset.symbol"].unique())
    all_status = sorted(df["state"].unique())
    # Sidebar filters
    st.sidebar.header("Filter Options")

    search_text = st.sidebar.text_input("Search Symbol", "")
    selected_status = st.sidebar.multiselect("Select Status", all_status, default=all_status)
    selected_types = st.sidebar.multiselect("Contract Type", all_contract_types, default=all_contract_types)
    selected_spots = st.sidebar.multiselect("Underlying Asset", all_spots, default=all_spots)

    # Apply filters on DataFrame
    filtered_df = df[
        df["state"].isin(selected_status) &
        df["contract_type"].isin(selected_types) &
        df["underlying_asset.symbol"].isin(selected_spots) 
    ]

    if search_text:
        filtered_df = filtered_df[filtered_df["symbol"].str.contains(search_text, case=False)].order_by('launch_time', ascending=False)
    st.subheader(f"Filtered Options: {len(filtered_df)} results")
    show_option_chain(filtered_df)
else:
    st.warning("No data to display.")
