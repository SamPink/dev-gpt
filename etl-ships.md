Here is the outline for the four Python files to create the data pipeline:

1. start.py
2. data.py
3. ETLScheduler.py
4. shipapi.py

Each file will perform specific tasks, as you mentioned. Let's start with the structure of each file and some initial code for each file.

1. start.py:

```python
import logging
import sys
from ETLScheduler import ETLScheduler


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

if __name__ == "__main__":
    setup_logging()
    logging.info("Starting ETL process")
    etl_scheduler = ETLScheduler()
    etl_scheduler.run()
```

2. data.py:

```python
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class ShipData(Base):
    __tablename__ = 'ship_data'
    
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer)
    ship_name = Column(String)
    ship_type = Column(String)
    lat = Column(Float)
    lon = Column(Float)

def get_session(connection_string):
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
```

3. ETLScheduler.py:

```python
import time
import logging
from data import ShipData, get_session
from shipapi import ShipAPI


class ETLScheduler:
    def __init__(self):
        self.session = get_session("sqlite:///ship_data.db")
        self.api = ShipAPI()

    def run(self):
        while True:
            logging.info("Starting ETL cycle")
            start_time = time.time()

            raw_data = self.api.get_data()
            self.transform_load_data(raw_data)

            end_time = time.time()
            logging.info(f"ETL cycle duration: {end_time - start_time} seconds")

            time.sleep(60)  # Run ETL cycle every minute

    def transform_load_data(self, raw_data):
        for ship in raw_data:
            ship_data = ShipData(
                ship_id=ship['ship_id'],
                ship_name=ship['ship_name'],
                ship_type=ship['ship_type'],
                lat=ship['lat'],
                lon=ship['lon']
            )
            self.session.add(ship_data)
            self.session.commit()
```

4. shipapi.py:

```python
import requests
import logging


class ShipAPI:
    def __init__(self):
        self.base_url = "https://marinetraffic.com/api/v1/"
        self.api_key = "your_api_key_here"

    def get_data(self):
        endpoint = f"{self.base_url}/get_ship_data?key={self.api_key}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            logging.error(f"Error fetching data from API: {response.text}")
            return []

        return self.parse_response(response)

    def parse_response(self, response):
        try:
            data = response.json()
            return data['data']
        except ValueError:
            logging.error(f"Error parsing API response: {response.text}")
            return []
```

Make sure to replace "your_api_key_here" with your actual API key.

This pipeline will fetch ship data from the ship API using `shipapi.py`, transform and load the data to your local/remote database using `ETLScheduler.py`, and utilize SQLAlchemy models in `data.py` to interact with the database. The `start.py` script brings it all together, scheduling the ETL process and setting up logging.