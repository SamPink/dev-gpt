import pandas as pd
import folium
from collections import Counter

# Load dataset and name columns
url = "http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv"
column_names = ['transaction_id', 'price', 'transfer_date', 'postcode', 'property_type', 'new_build', 'leasehold', 'PAON', 'SAON', 'street', 'locality', 'town_city', 'district', 'county', 'PPD_category', 'record_status']
data = pd.read_csv(url, header=None, names=column_names)

# Drop rows with missing data in relevant columns
data.dropna(subset=['postcode', 'town_city', 'street'], inplace=True)

# Count occurrences of each location (town/city, street)
location_counts = Counter(zip(data['town_city'], data['street']))

# Find the most popular location
most_popular_location, most_popular_count = location_counts.most_common(1)[0]

# Get the coordinates of the center of the most popular location
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="uk_property_map")
location = geolocator.geocode(f"{most_popular_location[1]}, {most_popular_location[0]}, UK")
center_lat, center_lon = location.latitude, location.longitude

# Create map centered on the most popular location
uk_property_map = folium.Map(location=[center_lat, center_lon], zoom_start=15)

# Add markers for properties in the most popular location
location_data = data[(data['town_city'] == most_popular_location[0]) & (data['street'] == most_popular_location[1])]
for _, row in location_data.iterrows():
    try:
        property_location = geolocator.geocode(f"{row['postcode']}, UK")
        folium.Marker([property_location.latitude, property_location.longitude], popup=f"Price: £{row['price']}").add_to(uk_property_map)
    except Exception as e:
        print(f"Failed to geocode: {row['postcode']}")

# Save the map to a file and display it
uk_property_map.save("uk_property_map.html")
uk_property_map