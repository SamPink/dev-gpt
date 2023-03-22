import requests
import json
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# OpenSky API credentials
USERNAME = "{{your_username}}"
PASSWORD = "{{your_password}}"

# SQLite database name
DB_NAME = "flights_db.sqlite"

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

# Flight model
class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True)
    icao24 = Column(String)
    callsign = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)

# Create table schema
Base.metadata.create_all(engine)

# Get flight data
def get_flights_near_london():
    url = f"https://opensky-network.org/api/states/all?lamin=51.29&lomin=-0.65&lamax=51.75&lomax=0.55"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    data = json.loads(response.text)
    
    # Limit the flights to 100 if more flights were retrieved.
    if len(data["states"]) > 100:
        data["states"] = data["states"][:100]
    
    return data["states"]

# ETL process
def etl_process(flights):
    # Truncate flights table
    session.query(Flight).delete()
    session.commit()

    # Insert flights data
    for flight_data in flights:
        flight = Flight(
            icao24=flight_data[0],
            callsign=flight_data[1],
            lat=flight_data[6],
            lon=flight_data[5],
            alt=flight_data[7]
        )

        session.add(flight)
    session.commit()

# Run the ETL
if __name__ == "__main__":
    flights_data = get_flights_near_london()
    etl_process(flights_data)