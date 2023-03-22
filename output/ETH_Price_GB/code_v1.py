import requests

def get_eth_price_gbp():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=gbp"
    response = requests.get(url)
    data = response.json()
    eth_price_gbp = data["ethereum"]["gbp"]
    return eth_price_gbp

eth_price_gbp = get_eth_price_gbp()
print(f"The current price of Ethereum (ETH) in GBP is: {eth_price_gbp}")