import requests

def get_eth_price_in_gbp():
    ETH_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=gbp"
    response = requests.get(ETH_URL)
    eth_price_data = response.json()
    eth_price_in_gbp = eth_price_data['ethereum']['gbp']
    return eth_price_in_gbp

if __name__ == "__main__":
    eth_price = get_eth_price_in_gbp()
    print(f"ETH price in GBP: £{eth_price}")