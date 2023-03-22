import requests
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Function to get data from the OpenSky Network API
def get_flight_data():
    API_URL = "https://opensky-network.org/api/states/all"
    response = requests.get(API_URL)
    data = response.json()

    columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact", "lng", "lat", "baro_altitude", "on_ground", "velocity", "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"]
    flights_df = pd.DataFrame(data['states'], columns=columns)

    # London Airports latitude and longitude
    london_airports_coords = [
        (51.470022, -0.454295),  # Heathrow Airport (EGLL)
        (51.505278, 0.055278),  # London City Airport (EGLC)
        (51.148056, -0.190278),  # Gatwick Airport (EGKK)
        (51.885000, 0.235000),  # Stansted Airport (EGSS)
        (51.874722, -0.368333),  # Luton Airport (EGGW)
        (51.571389, 0.695556)  # Southend Airport (EGMC)
    ]
    
    def is_near_london_airports(row):
        lat, lng = row['lat'], row['lng']
        for airport_lat, airport_lng in london_airports_coords:
            dist_sq = (airport_lat - lat) ** 2 + (airport_lng - lng) ** 2
            if dist_sq < 1.0:  # Roughly a square of 100 km side-length
                return True
        return False

    # Filter flights
    flights_df = flights_df[flights_df.apply(is_near_london_airports, axis=1)]

    # Keep only the most recent 100 flights
    flights_df = flights_df.sort_values('last_contact', ascending=False).head(100)
    
    return flights_df.dropna(subset=['lat', 'lng'])

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Real-Time Flight Tracker - London Airports"),
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0),  # Update every 30 seconds
    dbc.Row([
        dbc.Col(dcc.Graph(id="flight-map"), md=12)
    ]),
], fluid=True)

@app.callback(Output("flight-map", "figure"), [Input("interval-component", "n_intervals")])
def update_flight_map(n):
    flights_df = get_flight_data()
    fig = px.scatter_geo(flights_df, lat="lat", lon="lng", hover_name="callsign", projection="orthographic")
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, showocean=True)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":30})
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)