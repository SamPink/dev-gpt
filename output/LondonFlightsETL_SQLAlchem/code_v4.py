import os
import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set environment variable to silence SQLAlchemy warning
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"

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
    url = "https://adsbexchange-com1.p.rapidapi.com/json/lat/51.50/lng/-0.11/dist/30/"
    headers = {
        "X-RapidAPI-Key": "f5d2e2aaedomshb6d727ed6a8d6ap1e86e9jsn13261willremainconfidential",
        "X-RapidAPI-Host": "adsbexchange-com1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching flight data: {response.status_code}")
        return []

    data = json.loads(response.text)

    # Limit the flights to 100 if more flights were retrieved.
    if len(data["ac"]) > 100:
        data["ac"] = data["ac"][:100]

    return data["ac"]

# ETL process
def etl_process(flights):
    # Truncate flights table
    session.query(Flight).delete()
    session.commit()

    # Insert flights data
    for flight_data in flights:
        flight = Flight(
            icao24=flight_data["icao"],
            callsign=flight_data["call"],
            lat=flight_data["lat"],
            lon=flight_data["lon"],
            alt=flight_data["alt"]
        )

        session.add(flight)
    session.commit()

# Run the ETL
if __name__ == "__main__":
    flights_data = get_flights_near_london()
    etl_process(flights_data)