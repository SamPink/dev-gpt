# start.py
import logging
from ETLScheduler import ETLScheduler


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    etl_scheduler = ETLScheduler()
    etl_scheduler.start()

# data.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


class ShipData(Base):
    __tablename__ = 'ship_data'

    id = Column(Integer, primary_key=True)
    ship_name = Column(String)
    ship_type = Column(String)
    imo_number = Column(String)
    eta = Column(DateTime)
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


class DataAccess:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def add_data(self, data):
        session = self.Session()
        try:
            for row in data:
                session.add(ShipData(ship_name=row[0], ship_type=row[1], imo_number=row[2], eta=row[3]))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_data(self):
        session = self.Session()
        try:
            data = session.query(ShipData).all()
            return data
        except:
            session.rollback()
            raise
        finally:
            session.close()

# shipapi.py
import requests


def get_ship_data():
    api_url = 'http://example.com/'
    response = requests.get(api_url)
    data = response.json()
    return data

# ETLScheduler.py
import threading
from datetime import datetime, timedelta
from shipapi import get_ship_data
from data import DataAccess


class ETLScheduler:
    def __init__(self):
        self.data_access = DataAccess('sqlite:///ship.db')
        self.interval = 3600  # 1 hour
        self.timer = None

    def start(self):
        self.run_etl_process()
        self.schedule_etl_process()

    def run_etl_process(self):
        data = get_ship_data()
        self.data_access.add_data(data)

    def schedule_etl_process(self):
        self.timer = threading.Timer(self.interval, self.start)
        self.timer.daemon = True
        self.timer.start()