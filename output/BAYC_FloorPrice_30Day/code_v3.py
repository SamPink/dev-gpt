import requests
from datetime import datetime, timedelta

# Replace with your own OpenSea API key
API_KEY = 'YOUR_API_KEY'

# Bored Ape Yacht Club contract address
contract_address = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'

# Calculate the Unix timestamp of 30 days ago
timestamp_30_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())

# Prepare the API request URL
url = f'https://api.opensea.io/api/v1/events?asset_contract_address={contract_address}&event_type=successful&only_opensea=false&offset=0&limit=20&occurred_after={timestamp_30_days_ago}'

# Add your API key to headers
headers = {'X-API-KEY': API_KEY}

# Send the request
response = requests.get(url, headers=headers)

# Print the JSON data
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f"Error: {response.status_code}")

# Calculate the floor price using the response data
# ...