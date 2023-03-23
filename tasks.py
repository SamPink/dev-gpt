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

system_message= """
Act as a senior python dev and provide code in the following format: 

```bash
(required dependencies)
```

```python
(Python code)
```

the code should be in a single file that can be run from main"""