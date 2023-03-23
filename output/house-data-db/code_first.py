import pandas as pd
from sqlalchemy import create_engine

# Load data from CSV
url = 'http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv'
data = pd.read_csv(url)

# Rename the columns to have proper names
data = data.rename(
    columns={
        ',TransactionID': 'TransactionID',
        'Postcode': 'Postcode',
        'Price': 'Price',
        'TownCity': 'TownCity'
    }
)

# Create a SQLite database
engine = create_engine('sqlite:///uk_properties.db')

# Save the data into the database
data.to_sql('properties', engine, if_exists='replace', index=False)

# Query to find the top 10 most expensive properties in London
query = '''
SELECT * 
FROM properties 
WHERE TownCity = 'LONDON' 
ORDER BY Price DESC 
LIMIT 10
'''

# Execute the query and display the result
result = pd.read_sql_query(query, engine)
print(result)