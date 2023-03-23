import requests
import folium
import time

# Replace with your own coordinates:
latitude = 51.5074
longitude = -0.1278
min_latitude = latitude - 1
max_latitude = latitude + 1
min_longitude = longitude - 1
max_longitude = longitude + 1

# Function to get flights over the specified area
def get_flights_over_area(min_lat, max_lat, min_long, max_long):
    url = f"https://opensky-network.org/api/states/all?lamin={min_lat}&lamin={max_lat}&lomin={min_long}&lomin={max_long}"
    response = requests.get(url)
    data = response.json()
    return data["states"]

# Function to plot flights on an interactive map
def plot_flights_on_map(flights):
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    for flight in flights:
        if flight[5] is not None and flight[6] is not None:
            folium.Marker(
                location=[float(flight[6]), float(flight[5])],
                popup=f"ICAO24: {flight[0]}<br>Call Sign: {flight[1]}<br>Country: {flight[2]}",
                icon=folium.Icon(icon="plane", prefix="fa"),
            ).add_to(m)
    return m

# Plot the flights in real-time
while True:
    flights = get_flights_over_area(min_latitude, max_latitude, min_longitude, max_longitude)
    map_with_flights = plot_flights_on_map(flights)
    map_with_flights.save("real_time_flights_map.html")
    time.sleep(60)  # Update every 60 seconds, adjust this value for different update intervals