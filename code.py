import pandas as pd
from skyfield.api import Topos, load
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def get_starlink_satellites():
    stations_url = 'https://www.celestrak.com/NORAD/elements/starlink.txt'
    satellites = load.tle_file(stations_url)
    return satellites

def satellite_positions(satellites):
    positions = []

    ts = load.timescale()
    t = ts.now()

    for sat in satellites:
        geocentric = sat.at(t)
        subpoint = geocentric.subpoint()
        lat = subpoint.latitude.degrees
        lon = subpoint.longitude.degrees
        positions.append((sat.name, lat, lon))

    return positions

def plot_satellites(positions):
    df = pd.DataFrame(positions, columns=['Name', 'Latitude', 'Longitude'])

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scattergeo'}]])

    fig.add_trace(
        go.Scattergeo(
            lon=df['Longitude'],
            lat=df['Latitude'],
            mode='markers',
            marker=dict(size=4, color='red', symbol='circle'),
            text=df['Name'],
            showlegend=False,
        )
    )

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(title="Starlink Satellites")

    fig.show()

satellites = get_starlink_satellites()
positions = satellite_positions(satellites)
plot_satellites(positions)
subpoint = geocentric.subpoint()
lat = subpoint.latitude.degrees
lon = subpoint.longitude.degrees