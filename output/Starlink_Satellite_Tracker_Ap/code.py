import numpy as np
import pandas as pd
from skyfield.api import Topos, load
from skyfield.sgp4lib import EarthSatellite
import plotly.express as px

# Get TLE data for all Starlink satellites
starlink_tle_url = 'https://www.celestrak.com/NORAD/elements/starlink.txt'
satellites_txt = load.tle_file(starlink_tle_url)

# Get the position of each satellite
positions = []
for i in range(0, len(satellites_txt) - 1, 2):
    name = str(satellites_txt[i])
    line1 = str(satellites_txt[i + 1])
    line2 = str(satellites_txt[i + 2])

    satellite = EarthSatellite(line1, line2, name, load.timescale())
    geocentric = satellite.at(load.timescale().now())

    positions.append({
        'name': name,
        'x': geocentric.position.km[0],
        'y': geocentric.position.km[1],
        'z': geocentric.position.km[2],
    })

# Plot satellites on the globe using Plotly
df = pd.DataFrame(positions)
fig = px.scatter_3d(df, x='x', y='y', z='z', text='name')
fig.update_traces(marker=dict(size=5, colorscale='Viridis'))
fig.show()