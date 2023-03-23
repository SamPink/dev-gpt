import requests
import folium
from folium.plugins import HeatMap

# Coordinates for multiple locations in England
locations = [
    {"name": "London", "lat": 51.5074, "lng": -0.1278},
    {"name": "Manchester", "lat": 53.4808, "lng": -2.2426},
    {"name": "Birmingham", "lat": 52.4862, "lng": -1.8904},
    {"name": "Leeds", "lat": 53.8008, "lng": -1.5877},
    {"name": "Bristol", "lat": 51.4545, "lng": -2.5879}
]

# Fetch crime data for each location
all_crime_data = []
for location in locations:
    crime_data_url = f"https://data.police.uk/api/crimes-street/all-crime?lat={location['lat']}&lng={location['lng']}"
    response = requests.get(crime_data_url)

    if response.status_code == 200:
        crime_data = response.json()
        all_crime_data.extend(crime_data)
    else:
        print(f"Error fetching crime data for {location['name']}: {response.status_code}")

# Coordinates for the center of England
ENG_CENTER_COORDINATES = [52.3555, -1.1743]

# Create a map using the default OpenStreetMap tile server
map_instance = folium.Map(
    location=ENG_CENTER_COORDINATES,
    zoom_start=6,
    control_scale=True,
)

# Extract the latitude and longitude from the incident data
heatmap_data = [
    (float(incident["location"]["latitude"]), float(incident["location"]["longitude"]))
    for incident in all_crime_data
]

# Add the heatmap layer to the map
HeatMap(heatmap_data, radius=12).add_to(map_instance)

# Save the map to an HTML file
map_instance.save("crime_heatmap.html")