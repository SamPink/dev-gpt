import requests
import sqlite3

def create_bike_points_table(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS bike_points (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lon REAL)')

def create_crime_table(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS crimes (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, location_lon REAL, location_lat REAL, street_name TEXT, outcome_status TEXT, date TEXT)')

def insert_bike_point(conn, point):
    conn.execute('INSERT INTO bike_points (id, name, lat, lon) VALUES (?, ?, ?, ?)', (point['id'], point['commonName'], point['lat'], point['lon']))
    conn.commit()

def insert_crime(conn, crime):
    conn.execute('INSERT INTO crimes (category, location_lon, location_lat, street_name, outcome_status, date) VALUES (?, ?, ?, ?, ?, ?)', (crime['category'], crime['location']['longitude'], crime['location']['latitude'], crime['location']['street']['name'], crime['outcome_status']['category'], crime['month']))
    conn.commit()

def load_bike_points(conn):
    response = requests.get('https://api.tfl.gov.uk/BikePoint')
    
    if response.status_code != 200:
        print('Failed to load TfL bike points.')
        return
    
    data = response.json()
    
    for item in data:
        point = {
            'id': item['id'].split('_')[-1],
            'commonName': item['commonName'],
            'lat': item['lat'],
            'lon': item['lon']
        }
        insert_bike_point(conn, point)

def load_crime_data(conn):
    payload = {
        'lat': '51.5074',
        'lng': '-0.1277',
        'date': '2020-01'
    }
    response = requests.get('https://data.police.uk/api/crimes-street/all-crime', params=payload)
    
    if response.status_code != 200:
        print('Failed to load UK Police street-level crime data.')
        return
    
    crime_data = response.json()

    for crime in crime_data:
        if 'category' in crime and 'location' in crime and 'latitude' in crime['location'] and 'longitude' in crime['location']:
            insert_crime(conn, crime)

def main():    
    with sqlite3.connect('london_data.db') as conn:
        print('Creating tables...')
        create_bike_points_table(conn)
        create_crime_table(conn)
        
        print('Loading TfL bike points...')
        load_bike_points(conn)
        
        print('Loading UK Police street-level crime data...')
        load_crime_data(conn)

        print('Finished loading data.')

main()