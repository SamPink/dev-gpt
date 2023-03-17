from skyfield.api import Topos, load
import plotly.graph_objs as go

# Load satellite data from Celestrak
stations_url = 'http://celestrak.com/NORAD/elements/starlink.txt'
satellites = load.tle_file(stations_url)

# Load a timescale object to calculate the satellite positions
ts = load.timescale()

# Get the positions of the satellites
sat_positions = []

for satellite in satellites[:20]:  # Track only the first 20 satellites for simplicity
    eci = satellite.at(ts.now())
    lon = eci.subpoint().longitude.degrees
    lat = eci.subpoint().latitude.degrees
    sat_positions.append((lon, lat))

# Prepare the Globe
globe = go.Figure(go.Scattergeo())

# Draw the coastlines
globe.update_geos(showland=True, landcolor="rgb(243, 243, 243)",
                  showocean=True, oceancolor="rgb(0, 0, 255)",
                  showlakes=True, lakecolor="rgb(127, 205, 255)",
                  showrivers=True, rivercolor="rgb(127, 205, 255)",
                  showcountries=True, countrycolor="rgb(204, 204, 204)")

# Plot the satellite positions
for lon, lat in sat_positions:
    globe.add_trace(go.Scattergeo(lon=[lon], lat=[lat],
                                  mode='markers', marker=dict(color='red', size=6)))

# Set the title
globe.update_layout(title='Starlink Satellites on Globe')

# Show the plot
globe.show()