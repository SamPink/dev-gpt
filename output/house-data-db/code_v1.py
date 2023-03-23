import time
import requests
import folium
from IPython.display import clear_output

# Coordinate limits for the Maidenhead area
MIN_LATITUDE = 51.383
MAX_LATITUDE = 51.434
MIN_LONGITUDE = -0.635
MAX_LONGITUDE = -0.563

# OpenSky API URL
OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

def get_flights():
    response = requests.get(OPENSKY_API_URL)
    data = response.json()

    flights = []

    if 'states' in data:
        for state in data['states']:
            lat, lon = state[6], state[5]
            if MIN_LATITUDE <= lat <= MAX_LATITUDE and MIN_LONGITUDE <= lon <= MAX_LONGITUDE:
                flights.append({
                    'icao24': state[0],
                    'call_sign': state[1],
                    'origin_country': state[2],
                    'latitude': lat,
                    'longitude': lon,
                    'velocity': state[9],
                    'heading': state[10]
                })

    return flights

def draw_map(flights):
    map = folium.Map(location=[51.408, -0.599], zoom_start=13)

    for flight in flights:
        folium.Marker(
            location=[flight['latitude'], flight['longitude']],
            popup=f"{flight['call_sign']} ({flight['icao24']})",
            tooltip=f"{flight['call_sign']} ({flight['icao24']})",
            icon=folium.Icon(color='red', icon='plane', prefix='fa')
        ).add_to(map)

    return map

if __name__ == "__main__":
    while True:
        flights = get_flights()
        map = draw_map(flights)
        clear_output(wait=True)
        display(map)
        time.sleep(60)  # Update flight positions every minute