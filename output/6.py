import requests
import pandas as pd

def get_flights_near_london():
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": 50.823005, "lomin": -0.615978,
        "lamax": 51.835774, "lomax": 0.323161
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    open_sky_columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact", "longitude", "latitude", "baro_altitude", "on_ground", "velocity", "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"]
    df = pd.DataFrame(data['states'], columns=open_sky_columns)
    df = df.drop(['origin_country', 'time_position', 'last_contact', 'on_ground', 'sensors', 'squawk', 'spi', 'position_source'], axis=1)
    df = df[df["latitude"].notna() & df["longitude"].notna()]
    return df

flights_near_london = get_flights_near_london()
print(flights_near_london)