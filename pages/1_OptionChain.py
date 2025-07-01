import streamlit as st
import requests
import pandas as pd

st.title("Option Chain Visualization")

url = "https://api.india.delta.exchange/v2/products?contract_types=call_options,put_options&states=expired"

r = requests.get(url)
def show_option_chain(df):
    for idx, row in df.iterrows():
        symbol = row["symbol"]
        col1, col2 = st.columns([4, 1])
        st.write(f"[{symbol}](./Candlestick_Chart?symbol={symbol})") 
if r.ok:
    api_data = r.json()
    # st.write("Raw API Response:", api_data)
    # Once you know the structure, normalize/flatten and display
    # Example only if the API returns a 'result' with a list of dicts:
    products = api_data.get("result", [])
    df = pd.json_normalize(products)
    df = df[["id", "symbol","strike_price" ,"contract_type", "state", "description", "maker_commission_rate","taker_commission_rate","short_description",]]
    show_option_chain(df)
else:
    st.error("Failed to fetch data from Delta Exchange API.")
