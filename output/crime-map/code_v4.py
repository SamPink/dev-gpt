import requests
import folium
import json
from folium.plugins import HeatMap

# Replace with your HMLR API key
HMLR_API_KEY = "your_hmlr_api_key"

# Fetch house price data for the specified location
def fetch_house_price_data(location):
    api_url = f"https://lr-api.data-gov.uk/v1/ppd/?property_type=detached&min_price=50000&max_price=1000000&postcode_prefix={location['postcode']}&size=100"
    headers = {"Authorization": f"Bearer {HMLR_API_KEY}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        house_prices = response.json()
        return house_prices["data"]
    else:
        print(f"Error fetching house price data for {location['name']}: {response.status_code}")
        return []

# Fetch house price data for each location
all_house_price_data = []
for location in locations:
    house_price_data = fetch_house_price_data(location)
    all_house_price_data.extend(house_price_data)

# Calculate the average house price for each location
house_price_averages = []
for location in locations:
    house_prices = [float(house["price"]) for house in all_house_price_data if house["postcode"].startswith(location["postcode"])]
    if house_prices:
        house_price_averages.append({
            "name": location["name"],
            "lat": location["lat"],
            "lng": location["lng"],
            "average_price": sum(house_prices) / len(house_prices)
        })

# Create a map using the default OpenStreetMap tile server
map_instance = folium.Map(
    location=ENG_CENTER_COORDINATES,
    zoom_start=6,
    control_scale=True,
)

# Add the crime heatmap layer to the map
HeatMap(heatmap_data, radius=12).add_to(map_instance)

# Add markers for house price averages
for location in house_price_averages:
    folium.Marker(
        location=[location["lat"], location["lng"]],
        icon=None,
        popup=f"{location['name']}: £{location['average_price']:.2f}",
    ).add_to(map_instance)

# Save the map to an HTML file
map_instance.save("crime_heatmap_house_prices.html")
locations = [
    {"name": "London", "lat": 51.5074, "lng": -0.1278, "postcode": "SW1"},
    {"name": "Manchester", "lat": 53.4808, "lng": -2.2426, "postcode": "M1"},
    {"name": "Birmingham", "lat": 52.4862, "lng": -1.8904, "postcode": "B1"},
    {"name": "Leeds", "lat": 53.8008, "lng": -1.5877, "postcode": "LS1"},
    {"name": "Bristol", "lat": 51.4545, "lng": -2.5879, "postcode": "BS1"}
]