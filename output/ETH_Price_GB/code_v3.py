import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_crypto_prices_for_past_2_years(crypto_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range?vs_currency=gbp&from={start_timestamp}&to={end_timestamp}"

    response = requests.get(url)
    data = response.json()
    
    crypto_prices_gbp = [price_point[1] for price_point in data["prices"]]
    timestamp_dates = [price_point[0] for price_point in data["prices"]]
    
    return timestamp_dates, crypto_prices_gbp

def plot_crypto_prices(timestamp_dates, eth_prices_gbp, btc_prices_gbp):
    dates = [datetime.fromtimestamp(ts // 1000) for ts in timestamp_dates]
    
    plt.plot(dates, eth_prices_gbp, label="Ethereum (ETH)")
    plt.plot(dates, btc_prices_gbp, label="Bitcoin (BTC)")
    plt.xlabel("Date")
    plt.ylabel("Price in GBP")
    plt.title("Ethereum (ETH) vs. Bitcoin (BTC) Prices in GBP for the Past 2 Years")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

timestamp_dates, eth_prices_gbp = get_crypto_prices_for_past_2_years("ethereum")
_, btc_prices_gbp = get_crypto_prices_for_past_2_years("bitcoin")
plot_crypto_prices(timestamp_dates, eth_prices_gbp, btc_prices_gbp)