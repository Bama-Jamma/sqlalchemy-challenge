import requests
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import numpy as np
from config import api_key



#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    lat = 21.3069  # Latitude for Hawaii
    lon = -157.8583  # Longitude for Hawaii
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # Request temperature in Celsius
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        current_temp_c = weather_data["main"]["temp"]
        current_temp_f = (current_temp_c * 9/5) + 32
        condition = weather_data["weather"][0]["description"]
    else:
        current_temp_c = "N/A"
        current_temp_f = "N/A"
        condition = "N/A"

    return (
        """
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    color: #333333;
                    margin: 50px;
                }}
                
                h1 {{
                    font-size: 36px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                
                h2 {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-top: 30px;
                    margin-bottom: 10px;
                }}
                
                h3 {{
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                    margin-bottom: 15px;
                }}
                
                a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to the Hawaii Climate Analysis API!</h1>
            <p>This API provides climate analysis for the beautiful islands of Hawaii.</p>
            
            <h2>Current Weather in Hawaii:</h2>
            <p>Temperature: {}°C / {}°F</p>
            <p>Condition: {}</p>
            
            <h2>Available Routes:</h2>
            
            <h3><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></h3>
            <p>Returns a JSON list of precipitation data for the dates between 8/23/2016 and 8/23/2017.</p>
            
            <h3><a href="/api/v1.0/stations">/api/v1.0/stations</a></h3>
            <p>Returns a JSON list of stations from the dataset.</p>
            
            <h3><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></h3>
            <p>Returns a JSON list of temperature observations (TOBS) for the dates between 8/23/2016 and 8/23/2017.</p>
            
            <h3><a href="/api/v1.0/<start>">/api/v1.0/&lt;start&gt;</a></h3>
            <p>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date. Replace &lt;start&gt; in the URL with a valid date in the format YYYY-MM-DD.</p>
            
            <h3><a href="/api/v1.0/<start>/<end>">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a></h3>
            <p>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the start and end dates (inclusive). Replace &lt;start&gt; and &lt;end&gt; in the URL with valid dates in the format YYYY-MM-DD.</p>
        </body>
        </html>
        """.format(current_temp_c, current_temp_f, condition))


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session()
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()
    
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session()
    
    results = session.query(Station.station).all()
    
    session.close()
    
    station_list = list(np.ravel(results))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session()
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == "USC00519281").all()
    
    session.close()
    
    tobs_data = {date: tobs for date, tobs in results}
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    session = Session()
    
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    
    session.close()
    
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    session = Session()
    
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)