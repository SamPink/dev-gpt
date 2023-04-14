import requests
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Replace 'your_api_key_here' with your OpenSky API key
apiKey = 'your_api_key_here'

def get_flights_from_heathrow(apiKey):
    # Heathrow ICAO code is "EGLL"
    url = 'https://opensky-network.org/api/states/all'
    params = {
        'icao24': '',
        'icao24': '',
        'time': '',
        'icao': ['EGLL'],
        'lamin': '',
        'lomin': '',
        'lamax': '',
        'lomax': ''
    }
    auth = (apiKey, '')
    response = requests.get(url, params=params, auth=auth)
    return response.json()

def coords_list(flights_data):
    latitudes, longitudes, altitudes = [], [], []
    for state in flights_data['states']:
        latitudes.append(state[6])
        longitudes.append(state[5])
        altitudes.append(state[7])
    return latitudes, longitudes, altitudes

def plot_realtime_map_of_heathrow_planes():
    flights_data = get_flights_from_heathrow(apiKey)
    latitudes, longitudes, altitudes = coords_list(flights_data)

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scattergeo'}]])
    fig.add_trace(go.Scattergeo(
        lon=longitudes,
        lat=latitudes,
        text=altitudes,
        mode='markers',
        marker={'size': 8, 'opacity': 0.8, 'color': 'blue'}
    ))
    fig.update_geos(
        resolution=50,
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="rgb(230, 255, 230)",
        countrycolor="rgb(255, 255, 255)",
        coastlinecolor="rgb(127, 255, 127)"
    )
    fig.show()

if __name__ == "__main__":
    plot_realtime_map_of_heathrow_planes()