import requests
from skyfield.api import Topos, load, EarthSatellite
import plotly.graph_objects as go
import pandas as pd


def get_starlink_tle_data():
    response = requests.get("https://www.celestrak.com/NORAD/elements/starlink.txt")
    tle_lines = response.text.strip().split("\n")

    satellites = {
        f"STARLINK-{tle_lines[i].strip()}": [tle_lines[i + 1], tle_lines[i + 2]]
        for i in range(0, len(tle_lines), 3)
    }
    return satellites


def get_satellite_positions(satellite_tle_data):
    ts = load.timescale()
    t = ts.now()
    observer = Topos('0 N', '0 E')

    sat_positions = []

    for sat_name, tle_data in satellite_tle_data.items():
        sat = EarthSatellite(tle_data[0], tle_data[1], sat_name)
        difference = sat - observer
        topocentric = difference.at(t)
        lat, lon, _ = topocentric.frame_latlon()
        sat_positions.append(
            {"satellite": sat_name, "lat": lat.degrees, "lon": lon.degrees}
        )

    return sat_positions


def plot_satellite_positions(sat_positions):
    df = pd.DataFrame(sat_positions)

    fig = go.Figure(
        go.Scattergeo(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            marker=dict(
                size=6,
                color="red",
                opacity=0.7,
            ),
            text=df["satellite"],
            hoverinfo="text"
        )
    )

    fig.update_geos(
        showcountries=True, 
        showcoastlines=True,
        showland=True, 
        landcolor="rgb(235, 235, 235)",
        countrycolor="rgb(200, 200, 200)"
    )
    fig.update_layout(title="Starlink Satellites on a Globe", geo=dict(showframe=False, scope="world"))

    fig.show()


def main():
    starlink_satellites_tle = get_starlink_tle_data()
    satellite_positions = get_satellite_positions(starlink_satellites_tle)
    plot_satellite_positions(satellite_positions)


if __name__ == "__main__":
    main()