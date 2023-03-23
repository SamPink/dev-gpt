import pandas as pd

def read_price_paid_data(filename):
    # Read CSV with custom header
    column_names = ['TransactionID', 'Price', 'DateOfTransfer', 'Postcode', 'PropertyType',
                    'OldNew', 'Duration', 'PAON', 'SAON', 'Street', 'Locality',
                    'TownCity', 'District', 'Country', 'PPDCategoryType', 'RecordStatus']
    data = pd.read_csv(filename, header=None, names=column_names, parse_dates=['DateOfTransfer'])

    return data

def display_most_recent_transactions(data, top_n=10):
    # sort by DateOfTransfer and pick most recent top_n transactions
    recent_transactions = data.sort_values('DateOfTransfer', ascending=False).head(top_n)

    for _, row in recent_transactions.iterrows():
        print(f"Date: {row['DateOfTransfer'].strftime('%Y-%m-%d')}, Address: {row['PAON']} {row['Street']} {row['Postcode']}, Price: £{row['Price']}, Property Type: {row['PropertyType']}")

if __name__ == "__main__":
    filename = "price_paid_data.csv"  # replace with your csv file obtained from HM Land Registry
    data = read_price_paid_data(filename)
    display_most_recent_transactions(data)