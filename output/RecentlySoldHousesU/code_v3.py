import pandas as pd
import requests
from io import StringIO

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

def display_most_recent_transactions(data, top_n=10):
    recent_transactions = data.sort_values('DateOfTransfer', ascending=False).head(top_n)

    for _, row in recent_transactions.iterrows():
        print(f"Date: {row['DateOfTransfer'].strftime('%Y-%m-%d')}, Address: {row['PAON']} {row['Street']} {row['Postcode']}, Price: £{row['Price']}, Property Type: {row['PropertyType']}")

if __name__ == "__main__":
    url = "http://prod2.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2022.csv"  # replace with the latest URL from HM Land Registry
    data = download_price_paid_data(url)
    df = read_price_paid_data(data)
    display_most_recent_transactions(df)