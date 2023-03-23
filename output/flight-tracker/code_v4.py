import requests
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Replace with your own coordinates:
latitude = 51.5074
longitude = -0.1278
min_latitude = latitude - 1
max_latitude = latitude + 1
min_longitude = longitude - 1
max_longitude = longitude + 1

# Replace with your own Mapbox access token (https://www.mapbox.com)
MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoic3BpbmsiLCJhIjoiY2xlN2hxZW00MDBvZjNwc2NyMmNzZXc0cCJ9.V47jC5udtxn8P13fPNeXOA"

def get_flights_over_area(min_lat, max_lat, min_long, max_long):
    url = f"https://opensky-network.org/api/states/all?lamin={min_lat}&lamax={max_lat}&lomin={min_long}&lomax={max_long}"
    response = requests.get(url)
    data = response.json()
    return data.get("states", [])

def get_flight_dataframe():
    flights = get_flights_over_area(min_latitude, max_latitude, min_longitude, max_longitude)
    df = pd.DataFrame(
        flights, columns=["icao24", "callsign", "origin_country", "time_position", "last_contact", "long", "lat", "baro_altitude", "on_ground", "velocity", "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"])
    return df

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Real-Time Flights Over Area'),
    dcc.Interval(
        id='interval-component',
        interval=60 * 1000,  # Update every 60 seconds
        n_intervals=0
    ),
    dcc.Graph(id='flight-map')
])

@app.callback(Output('flight-map', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map(n):
    df = get_flight_dataframe()
    data = go.Scattermapbox(
        lat=df["lat"],
        lon=df["long"],
        mode='markers',
        marker=dict(size=7),
        text=df["callsign"],
        hoverinfo="text",
    )

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center=dict(lat=latitude, lon=longitude),
            zoom=8,
            style='dark'
        ),
    )

    return dict(data=[data], layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)