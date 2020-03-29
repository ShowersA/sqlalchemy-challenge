import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#weather app
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")    
def stations():

    list_stations = session.query(Station.station).all() 

    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    query_results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

        tobs = list(np.ravel(query_results))

        return jsonify(tobs)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
           query_results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        tobs = list(np.ravel(results))
        return jsonify(tobs)

    
    query_results = session.query(*select).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    tobs = list(np.ravel(query_results))
    return jsonify(tobs)

if __name__ == "__main__":
    app.run(debug=True)
