import requests
import json

def get_last_bayc_sold():
    url = "https://api.opensea.io/api/v1/events"
    query = {
        "event_type": "successful",
        "only_opensea": "false",
        "offset": "0",
        "limit": "1",
        "collection_slug": "boredapeyachtclub",
    }
    response = requests.get(url, params=query)
    data = response.json()

    if len(data["asset_events"]) > 0:
        last_sold = data["asset_events"][0]
        return {
            "token_id": last_sold["asset"]["token_id"],
            "name": last_sold["asset"]["name"],
            "image_url": last_sold["asset"]["image_url"],
            "price_in_eth": float(last_sold["total_price"]) / (10 ** 18),
            "transaction_timestamp": last_sold["transaction"]["timestamp"],
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