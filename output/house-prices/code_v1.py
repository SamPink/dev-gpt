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
# Dummy data (use real data from the sources mentioned above)
data = {
    'name': ['locationA', 'locationB'],
    'latitude': [51.507222, 51.523611],
    'longitude': [-0.127500, -0.156944],
    'proximity_to_public_transportation': [0.8, 0.7],
    'proximity_to_schools': [0.9, 0.6],
    'proximity_to_parks': [0.7, 0.4],
    'crime_rate': [0.2, 0.5],
    'access_to_healthcare': [0.5, 0.6],
}

df = pd.DataFrame(data)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude)
)

# Step 3: Visualize the data
mapbox_token = 'your_mapbox_access_token'
gdf["scaled_crime_rate"] = 1 - StandardScaler().fit_transform(df["crime_rate"].values.reshape(-1, 1))

color_stops = create_color_stops([0.0, 0.25, 0.5, 0.75, 1.0], colors='YlOrRd')

viz = GraduatedCircleViz(
    gdf,
    access_token=mapbox_token,
    weight_property="scaled_crime_rate",
    weight_stops=create_numeric_stops([0.0, 0.25, 0.5, 0.75, 1.0], 0.1),
    color_property="scaled_crime_rate",
    color_stops=color_stops,
    center=(-0.1275, 51.5072),
    zoom=9
)

viz.show()

# Step 4: Analyze data
X = gdf.drop(['name', 'latitude', 'longitude', 'geometry'], axis=1)

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
gdf['cluster'] = kmeans.labels_

# Step 5: Build a basic recommendation system
def calc_score(row, weights):
    score = 0
    for k, w in weights.items():
        score += row[k] * w
    return score

gdf['score'] = gdf.apply(calc_score, axis=1, args=(criteria,))
gdf = gdf.sort_values('score', ascending=False)
top_recommendations = gdf.head(3)

print("Top 3 recommended locations:")
print(top_recommendations)