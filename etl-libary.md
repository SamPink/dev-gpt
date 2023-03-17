Here's the library with 4 main classes - DataAccessLayer, EtlScheduler, ExternalApi and Server:

```python
# data_pipeline_lib.py
import requests
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends

Base = declarative_base()


class DataAccessLayer:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_or_update(self, model):
        session = self.Session()
        try:
            session.merge(model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def read_table(self, model):
        session = self.Session()
        try:
            result = session.query(model).all()
            return result
        finally:
            session.close()


class EtlScheduler(ABC):
    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, transformed_data):
        pass

    def start_etl(self):
        data = self.extract()
        transformed_data = self.transform(data)
        self.load(transformed_data)


class ExternalApi:
    def get_data_from_api(self, url, api_key, headers=None):
        if headers:
            headers.update({"apikey": api_key})
        else:
            headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        return response.json()


class Server:
    def __init__(self, etl_scheduler: EtlScheduler, data_access_layer: DataAccessLayer):
        self.app = FastAPI()
        self.etl_scheduler = etl_scheduler
        self.data_access_layer = data_access_layer

    def run_etl_job(self):
        self.etl_scheduler.start_etl()

    def read_data(self, model):
        return self.data_access_layer.read_table(model)

    def add_routes(self):
        @self.app.get("/run_etl")
        async def run_etl():
            self.run_etl_job()
            return {"status": "success"}

        @self.app.get("/{table_name}")
        async def get_data(table_name: str):
            if model := self.etl_scheduler.table_mapping.get(table_name):
                data = self.read_data(model)
                return data
            return {"error": f"Unknown table '{table_name}'"}

    def start_fastapi_server(self, host, port):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)
```

Now, an example implementation of the library, using ship data from marinetraffic.com:

```python
import os
from data_pipeline_lib import DataAccessLayer, EtlScheduler, ExternalApi, Server
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ship(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True)
    mmsi = Column(Integer, unique=True)
    name = Column(String)

    def __repr__(self):
        return f'Ship(id={self.id!r}, mmsi={self.mmsi!r}, name={self.name!r})'


class ShipEtlScheduler(EtlScheduler):
    def __init__(self, external_api, data_access_layer):
        self.external_api = external_api
        self.data_access_layer = data_access_layer
        self.table_mapping = {"ships": Ship}

    def extract(self):
        url = "https://services.marinetraffic.com/api/exportvessel/v:8"
        api_key = os.environ["MARINE_TRAFFIC_API_KEY"]
        data = self.external_api.get_data_from_api(url, api_key)
        return data

    def transform(self, data):
        ships = []
        for item in data:
            ship = Ship(id=item["id"], mmsi=item["mmsi"], name=item["name"])
            ships.append(ship)
        return ships

    def load(self, transformed_data):
        for ship in transformed_data:
            self.data_access_layer.insert_or_update(ship)


if __name__ == "__main__":
    external_api = ExternalApi()
    data_access_layer = DataAccessLayer("sqlite:///ships.db")
    etl_scheduler = ShipEtlScheduler(external_api, data_access_layer)
    server = Server(etl_scheduler, data_access_layer)
    server.add_routes()
    server.start_fastapi_server("0.0.0.0", 8000)
```

In this example, we are using marinetraffic.com data. Please note that you must have an API key to access their data. Replace the `api_key` placeholder with your actual API key.