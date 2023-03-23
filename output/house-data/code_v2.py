import pandas as pd
import folium
import requests
from io import StringIO
import json


def get_data(url):
    # Download CSV data from the URL and store it in a Pandas DataFrame
    response = requests.get(url)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    return pd.read_csv(csv_data)


def group_by_district(data):
    return data.groupby(["District"]).agg({"Price": "mean", "TransactionID": "count"}).reset_index()


def plot_map(grouped_data):
    geo_json = requests.get("https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/gb/counties.geojson").json()
    sales_map = folium.Map(location=[53.480759, -2.242631], zoom_start=6)
    folium.Choropleth(
        geo_data=geo_json,
        data=grouped_data,
        columns=["District", "Price"],
        key_on="properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Average Property Price",
    ).add_to(sales_map)
    return sales_map


def main():
    data_url = "http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv"
    sales_data = get_data(data_url)
    grouped_data = group_by_district(sales_data)
    sales_map = plot_map(grouped_data)
    sales_map.save("property_sales_map.html")


if __name__ == "__main__":
    main()