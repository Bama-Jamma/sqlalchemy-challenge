from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
import numpy as np

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
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Returns a JSON list of precipitation data for the dates between 8/23/2016 and 8/23/2017<br/>"
        f"/api/v1.0/stations<br/>"
        f"Returns a JSON list of stations from the dataset<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Returns a JSON list of temperature observations (TOBS) for the dates between 8/23/2016 and 8/23/2017<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the start and end dates (inclusive)<br/>"
    )

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