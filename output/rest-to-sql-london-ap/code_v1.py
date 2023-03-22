import requests
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template_string

Base = declarative_base()

# Define the model for the air quality table
class AirQualityLdn(Base):
    __tablename__ = 'air_quality_ldn'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    no2 = Column(Float, nullable=False)
    particulate_matter = Column(Float, nullable=False)

# Create the database and table
engine = create_engine('sqlite:///london_air_quality.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Fetch data and update the table
def update_air_quality_table():
    url = "https://api.erg.ic.ac.uk/AirQuality/Data/Nowcast/Index/1/Hourly/"
    response = requests.get(url)
    data = response.json()
    date = pd.to_datetime(data["AirQualityIndexObs"][0]["@MeasurementDateGMT"])
    no2 = float(data["AirQualityIndexObs"][0]["Species"][0]["@AirQualityIndex"])
    particulate_matter = float(data["AirQualityIndexObs"][0]["Species"][1]["@AirQualityIndex"])

    new_entry = AirQualityLdn(date=date, no2=no2, particulate_matter=particulate_matter)

    session = Session()
    session.add(new_entry)
    session.commit()
    session.close()

# Schedule table updates
def update_table_every_minute():
    while True:
        update_air_quality_table()
        time.sleep(60)

# Start the Flask app to display data on a web page
app = Flask(__name__)

@app.route('/')
def index():
    session = Session()
    data = session.query(AirQualityLdn).all()
    session.close()
    return render_template_string('''
        <table>
            <tr>
                <th>Date</th>
                <th>NO2</th>
                <th>Particulate Matter</th>
            </tr>
            {% for entry in data %}
            <tr>
                <td>{{ entry.date }}</td>
                <td>{{ entry.no2 }}</td>
                <td>{{ entry.particulate_matter }}</td>
            </tr>
            {% endfor %}
        </table>
    ''', data=data)

if __name__ == '__main__':
    # Start the table update thread in the background and the Flask app
    import threading
    update_table_thread = threading.Thread(target=update_table_every_minute, daemon=True)
    update_table_thread.start()
    
    app.run(debug=True)