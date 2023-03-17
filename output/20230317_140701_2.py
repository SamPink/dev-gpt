import requests

def get_eth_price():
    url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=GBP"
    response = requests.get(url)
    eth_price_gbp = response.json()['GBP']
    return eth_price_gbp

print(f"Current ETH price in £: {get_eth_price()}")