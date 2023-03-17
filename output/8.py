from skyfield.api import Topos, load
import matplotlib.pyplot as plt

# Load satellite data from Celestrak
stations_url = 'http://celestrak.com/NORAD/elements/starlink.txt'
satellites = load.tle_file(stations_url)

# Load a timescale object to calculate the satellite positions and observer location
ts = load.timescale()

# Set observer location (latitude, longitude) - example coordinates for New York
observer_location = Topos('40.7128 N', '74.0060 W')

# Prepare data for plotting
figure = plt.figure()
ax = figure.add_subplot(1, 1, 1)

for satellite in satellites[:20]:  # Track only the first 20 satellites for simplicity
    difference = satellite - observer_location
    topocentric = difference.at(ts.now())
    alt, az, distance = topocentric.altaz()

    if alt.degrees > 0:  # Satellite in observer's sky
        subpoint = topocentric.subpoint()
        ax.plot(subpoint.longitude.degrees, subpoint.latitude.degrees, 'bo', markersize=2)

# Set map parameters and display
ax.set_title('Starlink Satellites above the observer')
ax.set_xlabel('Longitude [degrees]')
ax.set_ylabel('Latitude [degrees]')
plt.show()