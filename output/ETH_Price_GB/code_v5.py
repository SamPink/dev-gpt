import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_top_5_cryptos():
    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url)
    data = response.json()
    return [d["item"]["id"] for d in data["coins"][:5]]

def get_historical_prices(crypto_list, years=5):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    historical_data = {}

    for crypto in crypto_list:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={end_date.timestamp()}"
        response = requests.get(url)
        data = response.json()
        historical_data[crypto] = pd.DataFrame(data["prices"], columns=["timestamp", crypto])

    return historical_data

def plot_historical_prices(historical_data):
    start_date = datetime.now() - timedelta(days=5 * 365)

    fig, ax = plt.subplots()
    for crypto, data in historical_data.items():
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
        data.set_index(["timestamp"], inplace=True)
        data[crypto].plot(ax=ax, label=crypto.upper())

    ax.set_xlim([start_date, datetime.now()])
    plt.xlabel("Years")
    plt.ylabel("USD")
    plt.title("Top 5 Cryptocurrencies Historical Prices")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    top_5_cryptos = get_top_5_cryptos()
    historical_data = get_historical_prices(top_5_cryptos)
    plot_historical_prices(historical_data)