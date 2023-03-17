import requests
import pandas as pd
from datetime import datetime

def get_eth_price_last_30_days():
    ENDPOINT = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    PARAMS = {
        "vs_currency": "gbp",
        "days": "30",
        "interval": "daily"
    }
    response = requests.get(ENDPOINT, params=PARAMS)
    data = response.json()
    prices = data["prices"]

    price_data = []
    for price in prices:
        timestamp, price_gbp = price
        date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        price_data.append([date, price_gbp])

    return price_data

def save_eth_price_last_30_days_to_csv(price_data):
    df = pd.DataFrame(price_data, columns=["Date", "ETH_Price_GBP"])
    df.to_csv("PriceOverLast30Days.csv", index=False)
    print("ETH price data for the last 30 days has been saved as 'PriceOverLast30Days.csv'")

if __name__ == "__main__":
    eth_prices_last_30_days = get_eth_price_last_30_days()
    save_eth_price_last_30_days_to_csv(eth_prices_last_30_days)