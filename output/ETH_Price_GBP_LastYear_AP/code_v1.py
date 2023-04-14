import requests
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"  # Replace with your API key from CryptoCompare
ETH_GBP_API_URL = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=GBP&limit=365&api_key={API_KEY}"

def get_eth_gbp_last_year():
    response = requests.get(ETH_GBP_API_URL)
    data = response.json()

    if data["Response"] == "Success":
        daily_prices = data["Data"]["Data"]
        total_price = 0
        for price_info in daily_prices:
            total_price += price_info["close"]

        average_price = total_price / len(daily_prices)
        print(f"Average ETH price in GBP for the last year: {average_price:.2f}")

    else:
        print("Error fetching data from CryptoCompare API")

if __name__ == "__main__":
    get_eth_gbp_last_year()