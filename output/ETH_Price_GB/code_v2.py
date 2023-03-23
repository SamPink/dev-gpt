import requests

def get_eth_price_in_gbp():
    url = "https://api.coinpaprika.com/v1/tickers/eth-ethereum"
    response = requests.get(url)
    data = response.json()
    eth_to_btc = data["quotes"]["BTC"]["price"]
    btc_to_gbp = data["quotes"]["GBP"]["price"]
    eth_to_gbp = eth_to_btc * btc_to_gbp
    return eth_to_gbp

if __name__ == "__main__":
    eth_price = get_eth_price_in_gbp()
    print("ETH Price in GBP: £{:.2f}".format(eth_price))