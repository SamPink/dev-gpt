import requests
import plotly.express as px
import pandas as pd

# Replace with your Opensky-network API credentials
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Fetch flight data from Opensky-network public API
def fetch_flight_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        data = response.json()
        return data['states']
    else:
        print("Error: Unable to fetch flight data")
        return []

# Preprocess flight data for plotting using Plotly
def preprocess_flight_data(flight_data):
    df = pd.DataFrame(flight_data, columns=['icao24', 'callsign', 'origin_country',
                                            'time_position', 'last_contact',
                                            'longitude', 'latitude', 'baro_altitude',
                                            'on_ground', 'velocity', 'true_track',
                                            'vertical_rate', 'sensors', 'geo_altitude',
                                            'squawk', 'spi', 'position_source'])
    df = df[['callsign', 'latitude', 'longitude', 'baro_altitude', 'velocity', 'origin_country']].dropna()
    df.columns = ['Call Sign', 'Latitude', 'Longitude', 'Altitude', 'Speed', 'Country']
    return df

# Plot flights on a globe using Plotly
def plot_flights_on_globe(flight_data):
    fig = px.scatter_geo(flight_data,
                         lat='Latitude',
                         lon='Longitude',
                         hover_name='Call Sign',
                         hover_data=['Altitude', 'Speed', 'Country'],
                         projection='natural earth')
    fig.show()

def main():
    flight_data = fetch_flight_data()
    if flight_data:
        flight_data_df = preprocess_flight_data(flight_data)
        plot_flights_on_globe(flight_data_df)

if __name__ == "__main__":
    main()