import requests
import pandas as pd
import sqlalchemy as db

def extract_data_from_api(url, params):
    response = requests.get(url, params=params)
    return response.json()

def json_to_dataframe(data):
    return pd.json_normalize(data)

def connect_to_database(db_url):
    engine = db.create_engine(db_url)
    connection = engine.connect()
    return engine, connection

def push_data_to_table(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def main(tfl_api_key, tfl_app_id, db_url):
    # TFL API URLs and parameters
    urls = {
        'tfl_stats': 'https://api.tfl.gov.uk/bikepoint',
    }

    params = {
        'tfl_stats': {'app_key': tfl_api_key, 'app_id': tfl_app_id},
    }

    # Obtain data from TFL API
    tfl_data = extract_data_from_api(urls['tfl_stats'], params['tfl_stats'])

    # Process the JSON data into a DataFrame
    tfl_df = json_to_dataframe(tfl_data)

    # Connect to the database
    engine, connection = connect_to_database(db_url)

    # Push the data to database table
    push_data_to_table(tfl_df, "tfl_bikepoints", engine)

    # Close connection
    connection.close()

if __name__ == '__main__':
    # Add your TFL API key, TFL App ID, and database URL in the following format:
    # postgresql://username:password@localhost/db_name
    tfl_api_key = "your_tfl_api_key"
    tfl_app_id = "your_tfl_app_id"
    db_url = "your_database_url"
    main(tfl_api_key, tfl_app_id, db_url)