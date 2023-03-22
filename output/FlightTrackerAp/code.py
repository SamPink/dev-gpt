import requests
import folium
from folium.plugins import MarkerCluster
import time

# Replace these with your own OpenSky Network credentials
USERNAME = "your_username"
PASSWORD = "your_password"

def get_flight_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, auth=(USERNAME, PASSWORD))

    flight_data = response.json()

    flight_list = []
    for flight in flight_data['states']:
        flight_position = {
            'icao24': flight[0],
            'callsign': flight[1].strip(),
            'lat': flight[6],
            'lon': flight[5],
            'altitude': flight[7],
            'origin_country': flight[2],
        }
        flight_list.append(flight_position)

    return flight_list


def create_map(flight_list):
    flight_map = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(flight_map)

    for flight in flight_list:
        if flight['lat'] and flight['lon'] and flight['callsign']:
            tooltip = f"{flight['callsign']} ({flight['origin_country']}), Altitude: {flight['altitude']} m"
            folium.Marker([flight['lat'], flight['lon']], tooltip=tooltip).add_to(marker_cluster)

    return flight_map


def main():
    while True:
        flight_list = get_flight_data()
        flight_map = create_map(flight_list)
        flight_map.save('flight_tracker.html')
        time.sleep(300)  # Update every 5 minutes

if __name__ == "__main__":
    main()