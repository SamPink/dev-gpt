import requests

def get_eth_gbp_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=gbp'
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        eth_gbp = json_data['ethereum']['gbp']
        return eth_gbp
    else:
        return None

eth_gbp_price = get_eth_gbp_price()
if eth_gbp_price is not None:
    print(f"The current price of 1 ETH in GBP is: £{eth_gbp_price}")
else:
    print("Unable to fetch the ETH price in GBP.")