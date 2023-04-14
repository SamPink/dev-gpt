import requests
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = "YOUR_API_KEY"  # Replace with your CryptoCompare API key

def fetch_price_history(symbol, currency="GBP", days=365):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym={currency}&limit={days}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "Success":
        return data["Data"]["Data"]
    else:
        st.error(f"Error fetching data for {symbol} from CryptoCompare API")
        return []

def plot_prices(selected_symbols):
    if not selected_symbols:
        st.error("Please select at least one cryptocurrency to plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    for symbol in selected_symbols:
        price_history = fetch_price_history(symbol)
        if price_history:
            dates = [datetime.fromtimestamp(price_info['time']) for price_info in price_history]
            close_prices = [price_info["close"] for price_info in price_history]
            ax.plot(dates, close_prices, label=symbol)

    ax.set_xlabel("Date (Last Year)")
    ax.set_ylabel("Price in GBP")
    ax.set_title(f"{', '.join(selected_symbols)} Prices in GBP Over the Last Year")
    ax.legend()
    st.pyplot(fig)

st.set_page_config(page_title="Crypto Price App", page_icon="🚀", layout="wide")
st.title("Cryptocurrency Prices Over the Last Year")
available_symbols = ["ETH", "BTC", "DOGE", "SOL"]

selected_symbols = st.multiselect("Select cryptocurrencies to plot:", available_symbols, default=["ETH", "BTC", "DOGE", "SOL"])

plot_prices(selected_symbols)