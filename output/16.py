ecef = sat.at(t).position.km
import requests
from skyfield.api import Topos, load, EarthSatellite
from skyfield import almanac
import plotly.express as px
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

    sat_positions = []

    for sat_name, tle_data in satellite_tle_data.items():
        sat = EarthSatellite(tle_data[0], tle_data[1], sat_name)
        ecef = sat.at(t).position.km
        sat_positions.append(
            {"satellite": sat_name, "x": ecef[0], "y": ecef[1], "z": ecef[2]}
        )

    return sat_positions


def plot_satellite_positions(sat_positions):
    df = pd.DataFrame(sat_positions)

    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="satellite",
        hover_name="satellite",
        title="Starlink Satellites in Earth-Centered Earth-Fixed (ECEF) Coordinates",
    )

    fig.show()


def main():
    starlink_satellites_tle = get_starlink_tle_data()
    satellite_positions = get_satellite_positions(starlink_satellites_tle)
    plot_satellite_positions(satellite_positions)


if __name__ == "__main__":
    main()