import requests
import folium
from folium.plugins import HeatMap

# Replace with your city information and polygon coordinates for your area of interest
CITY_NAME = "London"
COORDINATES = [51.5074, -0.1278]

# Get crime data (use a public API, in this example we use the UK Police API)
crime_data_url = "https://data.police.uk/api/crimes-street/all-crime?lat=51.5074&lng=-0.1278"
response = requests.get(crime_data_url)

# Check if the request was successful
if response.status_code == 200:
    crime_data = response.json()

    # Extract the latitude and longitude from the incident data
    heatmap_data = [
        (float(incident["location"]["latitude"]), float(incident["location"]["longitude"]))
        for incident in crime_data
    ]

    # Create a map using the default OpenStreetMap tile server
    map_instance = folium.Map(
        location=COORDINATES,
        zoom_start=13,
        control_scale=True
    )

    # Add the heatmap layer to the map
    HeatMap(heatmap_data, radius=12).add_to(map_instance)

    # Save the map to an HTML file
    map_instance.save("crime_heatmap.html")

else:
    print(f"Error fetching crime data: {response.status_code}")