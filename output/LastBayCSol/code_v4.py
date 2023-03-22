import requests
import json

def get_last_bayc_sold():
    url = "https://api.opensea.io/api/v1/assets"
    query = {
        "order_by": "sale_date",
        "order_direction": "desc",
        "limit": "50",
    }
    response = requests.get(url, params=query)

    if response.status_code != 200:
        print(f"Error: Unexpected API response. Status code: {response.status_code}")
        return None

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: Unable to parse API response as JSON.")
        return None

    last_sold = None
    for asset in data["assets"]:
        if asset["collection"]["slug"] == "boredapeyachtclub":
            last_sold = asset
            break

    if last_sold is not None:
        return {
            "token_id": last_sold["token_id"],
            "name": last_sold["name"],
            "image_url": last_sold["image_url"],
            "price_in_eth": float(last_sold["last_sale"]["total_price"]) / (10 ** 18),
            "transaction_timestamp": last_sold["last_sale"]["event_timestamp"],
        }
    else:
        return None

if __name__ == "__main__":
    last_bayc = get_last_bayc_sold()
    if last_bayc:
        print(f"Last BAYC NFT sold:\n"
              f"Token ID: {last_bayc['token_id']}\n"
              f"Name: {last_bayc['name']}\n"
              f"Image URL: {last_bayc['image_url']}\n"
              f"Price in ETH: {last_bayc['price_in_eth']}\n"
              f"Transaction Timestamp: {last_bayc['transaction_timestamp']}")
    else:
        print("No recent BAYC NFT sales found.")