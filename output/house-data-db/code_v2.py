import pandas as pd
import folium

# Load CSV data into a DataFrame
column_names = ['transaction_id', 'price', 'transfer_date', 'postcode', 'property_type', 'new_build', 'leasehold', 'PAON', 'SAON', 'street', 'locality', 'town_city', 'district', 'county', 'PPD_category', 'record_status']
data = pd.read_csv("data/house-data.csv", header=None, names=column_names)

# Filter properties in London
london_data = data[data['town_city'] == 'LONDON']

# Sort prices in descending order and select top 10
top_10_expensive_properties = london_data.sort_values(by='price', ascending=False).head(10)

# Define a function to get latitude and longitude from postcode
def get_lat_lng(postcode: str):
    import requests
    try:
        response = requests.get(f'http://api.postcodes.io/postcodes/{postcode}').json()
        if response['status'] == 200:
            lat, lng = response['result']['latitude'], response['result']['longitude']
            return lat, lng
    except:
        return None, None

# Create a map centered around London
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# Add markers for each property
for _, row in top_10_expensive_properties.iterrows():
    lat, lng = get_lat_lng(row['postcode'])
    if lat and lng:
        folium.Marker(location=[lat, lng],
                      tooltip=f"Price: £{row['price']}<br>Address: {row['PAON']} {row['street']}, {row['postcode']}"
                      ).add_to(m)

# Save the map to an HTML file
m.save("london_expensive_properties_map.html")