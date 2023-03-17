import requests

def get_eth_price_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        eth_price_usd = data["ethereum"]["usd"]
        print(f"Current price of Ethereum (ETH) in USD: ${eth_price_usd}")
    else:
        print("Error: Unable to fetch data from CoinGecko API")

get_eth_price_usd()
