import folium
import pandas as pd
import requests

# Function to fetch data from TFL API and return parsed JSON
def get_tfl_data(api_key):
    url = f"https://api.tfl.gov.uk/Place/Type/Junction?app_id={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Convert the JSON data to a DataFrame
def json_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

# Function to create the traffic map of London
def create_traffic_map(df, zoom_start=12):
    # Create map centered on London coordinates
    london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=zoom_start)

    # Add traffic junction markers to the map
    for index, row in df.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        name = row["commonName"]
        folium.Marker(location=[lat, lon], popup=name, icon=folium.Icon(color="red", icon="car")).add_to(london_map)

    return london_map

# Replace with your own API key from TFL API Portal
api_key = "<your_api_key>"

# Get parsed JSON data using the API key
tfl_data = get_tfl_data(api_key)

# Convert the data into a DataFrame
traffic_data = json_to_dataframe(tfl_data)

# Create the traffic map and save it as an HTML file
map_ = create_traffic_map(traffic_data)
map_.save("london_traffic_map.html")