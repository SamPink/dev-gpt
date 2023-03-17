import requests

# Define the API endpoint
url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract the ETH price in USD
    eth_price_usd = data["ethereum"]["usd"]

    # Print the ETH price in USD
    print("The current price of Ethereum (ETH) in USD is:", eth_price_usd)
else:
    print("Error: Unable to fetch price data. HTTP status code:", response.status_code)
