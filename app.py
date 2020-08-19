
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session from Python to the DB
session = Session(engine)

app = Flask(__name__)

date = "2016-08-23"

@app.route("/")
def home():
    return (
        f"<p>Welcome to the Hawaii Climate Analysis API!</p>"
        f"<p>Available Routes:</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/>"
        f"/api/v1.0/<start><br/>Returns a JSON list of the minimum, average , and maximum temperature for the dates between the start date and 8/23/17<br/>."
        f"/api/v1.0/<start>/<end><br/>Returns a JSON list of the minimum, average temperature, and maximum temperature between the given start date and end date<br/>."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= date).group_by(Measurement.date).all()
    return jsonify(prcp_results)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.name).all()
    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    temp_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= date).all()
    return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
def startDate(start):
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def startAndEnd(start,end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date
                             >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

if __name__ == "__main__":
    app.run(debug=True)

