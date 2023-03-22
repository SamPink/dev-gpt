import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_eth_prices_for_past_90_days():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=gbp&from={start_timestamp}&to={end_timestamp}"

    response = requests.get(url)
    data = response.json()
    
    eth_prices_gbp = [price_point[1] for price_point in data["prices"]]
    timestamp_dates = [price_point[0] for price_point in data["prices"]]
    
    return timestamp_dates, eth_prices_gbp

def plot_eth_prices(timestamp_dates, eth_prices_gbp):
    dates = [datetime.fromtimestamp(ts // 1000) for ts in timestamp_dates]
    
    plt.plot(dates, eth_prices_gbp)
    plt.xlabel("Date")
    plt.ylabel("Ethereum (ETH) Price in GBP")
    plt.title("Ethereum (ETH) Price in GBP for the Past 90 Days")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

timestamp_dates, eth_prices_gbp = get_eth_prices_for_past_90_days()
plot_eth_prices(timestamp_dates, eth_prices_gbp)