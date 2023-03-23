import pandas as pd
import geopandas as gpd
from mapboxgl.utils import create_color_stops
from mapboxgl.viz import GraduatedCircleViz
import requests
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Define your criteria
criteria = {
    'proximity_to_public_transportation': 0.3,
    'proximity_to_schools': 0.2,
    'proximity_to_parks': 0.3,
    'crime_rate': 0.1,
    'access_to_healthcare': 0.1,
}

# Step 2: Gather data
# Load property data from provided URL
url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv"
property_data = pd.read_csv(url, header=None)

# Preprocess the data
property_data = property_data.iloc[:, [2, 9, 10]]
property_data.columns = ['price', 'longitude', 'latitude']
property_data = property_data.dropna()
property_data = property_data.groupby(['latitude', 'longitude']).mean().reset_index()

# Convert to GeoDataFrame
property_gdf = gpd.GeoDataFrame(
    property_data, geometry=gpd.points_from_xy(property_data.longitude, property_data.latitude)
)

# Visualize the property data on a Mapbox map
mapbox_token = "pk.eyJ1Ijoic3BpbmsiLCJhIjoiY2xlN2hxZW00MDBvZjNwc2NyMmNzZXc0cCJ9.V47jC5udtxn8P13fPNeXOA"

color_stops = create_color_stops([0, 0.25, 0.5, 0.75, 1], colors='YlOrRd')

property_gdf["scaled_price"] = StandardScaler().fit_transform(property_gdf['price'].values.reshape(-1, 1))

viz = GraduatedCircleViz(
    property_gdf,
    access_token=mapbox_token,
    weight_property="scaled_price",
    weight_stops=create_numeric_stops([0, 0.25, 0.5, 0.75, 1], 0.1),
    color_property="scaled_price",
    color_stops=color_stops,
    center=(-0.1275, 51.5072),
    zoom=5
)

viz.show()