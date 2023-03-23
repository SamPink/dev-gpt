import requests
import folium
from folium.plugins import HeatMap

# Replace with your Mapbox API key
MAPBOX_API_KEY = "pk.eyJ1Ijoic3BpbmsiLCJhIjoiY2xlN2hxZW00MDBvZjNwc2NyMmNzZXc0cCJ9.V47jC5udtxn8P13fPNeXOA"

# Replace with your city information and polygon coordinates for your area of interest
CITY_NAME = "San Francisco"
COORDINATES = [37.7749, -122.4194]

# Get crime data (use a public API, in this example we use the SFPD API)
crime_data_url = "https://data.sfgov.org/resource/wg3w-h783.json"
response = requests.get(crime_data_url)

# Check if the request was successful
if response.status_code == 200:
    crime_data = response.json()

    # Extract the latitude and longitude from the incident data
    heatmap_data = [
        (float(incident["latitude"]), float(incident["longitude"]))
        for incident in crime_data
        if "latitude" in incident and "longitude" in incident
    ]
    
    # Create a Mapbox map
    map_instance = folium.Map(
        location=COORDINATES,
        zoom_start=13,
        tiles="https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{{z}}/{{x}}/{{y}}?access_token=" + MAPBOX_API_KEY,
        attr="Mapbox",
    )

    # Add the heatmap layer to the map
    HeatMap(heatmap_data, radius=12).add_to(map_instance)

    # Save the map to an HTML file
    map_instance.save("crime_heatmap.html")

else:
    print(f"Error fetching crime data: {response.status_code}")