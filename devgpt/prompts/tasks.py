house_data_task = """
there is a csv file called house-data.csv (it does not currently have any headers) in the data folder. it contains

this dataset of properties sold in the uk last year with 766k rows.

column_names = ['transaction_id', 'price', 'transfer_date', 'postcode', 'property_type', 'new_build', 'leasehold', 'PAON', 'SAON', 'street', 'locality', 'town_city', 'district', 'county', 'PPD_category', 'record_status']
    
write a query to find the top 10 most expensive properties in london
"""

flights_task = """
use a public api to get flights currently flying over the maidenhead.

plot this data on a interactive map.

the map should show the planes moving in real time.
"""

house_price = """
Great idea! Here are some steps to help you create a project that can help you decide where to buy a house in the UK:

Define your criteria: The first step is to define your criteria for selecting a location. This could include factors such as proximity to public transportation, schools, parks, crime rates, access to healthcare, and other amenities that are important to you.

Gather data: Once you have defined your criteria, you can start gathering data about different neighborhoods in the UK. You can use public datasets such as the UK Police Data, the UK government's OpenData portal, and the UK House Price Index. You can also use APIs such as Zoopla or Rightmove to gather data on house prices and other property-related information.

Visualize the data: After you have gathered the data, you can start visualizing it on a map using Mapbox. You can use different data layers to display information such as house prices, crime rates, and proximity to public transportation.

Analyze the data: Once you have visualized the data, you can start analyzing it to find patterns and correlations. For example, you can use clustering algorithms to group neighborhoods with similar characteristics, or you can use regression models to predict house prices based on different factors.

Build a recommendation system: Finally, you can build a recommendation system that takes into account your criteria and the data analysis results to suggest neighborhoods that match your preferences. This recommendation system can be based on machine learning algorithms such as collaborative filtering or content-based filtering.

By following these steps, you can create a powerful tool that helps you make informed decisions when buying a house in the UK.
"""

crime_map = """

mapbox api key "pk.eyJ1Ijoic3BpbmsiLCJhIjoiY2xlN2hxZW00MDBvZjNwc2NyMmNzZXc0cCJ9.V47jC5udtxn8P13fPNeXOA"
Crime heatmap - You can create a crime heatmap using Mapbox and public APIs such as the Crime Data API. This heatmap can display the frequency and intensity of crime incidents in a particular area or city. You can also add features such as filtering by crime type, time period, and demographic information.
"""

system_message= """
Act as a senior python dev and provide code in the following format: 

```bash
(required dependencies)
```

```python
(Python code)
```

the code should be in a single file that can be run from main.
never try to import any local files, or external apis that require a key.
the code should run without any aditional configuration.
follow all of these rules exactly or the code will not run.
"""