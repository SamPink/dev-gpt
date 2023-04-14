import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = "YOUR_API_KEY"  # Replace with your CryptoCompare API key

symbols = ["ETH", "BTC", "DOGE", "SOL"]
prices = {}

def fetch_price_history(symbol, currency="GBP", days=365):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym={currency}&limit={days}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["Response"] == "Success":
        return data["Data"]["Data"]
    else:
        print(f"Error fetching data for {symbol} from CryptoCompare API")
        return []

def plot_prices():
    for symbol in symbols:
        price_history = fetch_price_history(symbol)
        if price_history:
            prices[symbol] = price_history

    plt.figure(figsize=(12, 6))
    for symbol, price_history in prices.items():
        dates = [datetime.fromtimestamp(price_info['time']) for price_info in price_history]
        close_prices = [price_info["close"] for price_info in price_history]
        plt.plot(dates, close_prices, label=symbol)
    
    plt.xlabel("Date (Last Year)")
    plt.ylabel("Price in GBP")
    plt.title("ETH, BTC, DOGE, SOL Prices in GBP Over the Last Year")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_prices()