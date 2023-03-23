import pandas as pd
import requests
from io import StringIO
from geopy.geocoders import Nominatim
import folium

def download_price_paid_data(url):
    response = requests.get(url)
    response.raise_for_status()
    data = StringIO(response.text)
    return data

def read_price_paid_data(data):
    column_names = ['TransactionID', 'Price', 'DateOfTransfer', 'Postcode', 'PropertyType',
                    'OldNew', 'Duration', 'PAON', 'SAON', 'Street', 'Locality',
                    'TownCity', 'District', 'Country', 'PPDCategoryType', 'RecordStatus']
    data = pd.read_csv(data, header=None, names=column_names, parse_dates=['DateOfTransfer'])
    return data

def geocode_address(geolocator, address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None

def create_map(df, top_n=100):
    geolocator = Nominatim(user_agent="recent_property_sales")

    m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)  # Set the initial location to London

    for _, row in df.head(top_n).iterrows():
        full_address = f"{row['PAON']} {row['Street']} {row['Postcode']}"
        lat, lon = geocode_address(geolocator, full_address)

        if lat and lon:
            folium.Marker(
                [lat, lon],
                popup=f"Date: {row['DateOfTransfer'].strftime('%Y-%m-%d')}<br>Address: {full_address}<br>Price: £{row['Price']}<br>Property Type: {row['PropertyType']}",
                tooltip=full_address,
            ).add_to(m)

    return m

if __name__ == "__main__":
    url = "http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv"  # replace with the latest URL from HM Land Registry
    data = download_price_paid_data(url)
    df = read_price_paid_data(data)
    
    # Get the most recent sales
    df = df.sort_values('DateOfTransfer', ascending=False)

    # Create a map with markers for the most recent sales
    sales_map = create_map(df)
    sales_map.save("recent_property_sales.html")