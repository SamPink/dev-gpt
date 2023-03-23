import requests

def get_eth_price_in_gbp():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=gbp"
    response = requests.get(url)
    data = response.json()
    eth_to_gbp = data["ethereum"]["gbp"]
    return eth_to_gbp

if __name__ == "__main__":
    eth_price = get_eth_price_in_gbp()
    print("ETH Price in GBP: £{:.2f}".format(eth_price))