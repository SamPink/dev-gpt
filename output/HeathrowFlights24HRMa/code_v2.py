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
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data from OpenSky API. Status code: {response.status_code}")
        return None

def coords_list(flights_data):
    latitudes, longitudes, altitudes = [], [], []
    
    if flights_data and "states" in flights_data:
        for state in flights_data['states']:
            latitudes.append(state[6])
            longitudes.append(state[5])
            altitudes.append(state[7])
    
    return latitudes, longitudes, altitudes

def plot_realtime_map_of_heathrow_planes():
    flights_data = get_flights_from_heathrow(apiKey)
    
    if flights_data:
        latitudes, longitudes, altitudes = coords_list(flights_data)
    else:
        print("No flights data was available")
        return

    # Rest of the code remains the same