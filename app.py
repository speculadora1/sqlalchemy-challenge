# import dependencies
import numpy as np
from datetime import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################### 
# Database Setup 
#########################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#########################################################
# Flask App Setup
#########################################################
climateApp = Flask(__name__)


#########################################################
# Flask Routes
#########################################################

# HOME ROUTE
@climateApp.route("/")
def home():
    print("Server received request for 'Home' page...")
    
    # list available routes
    return (
        f"Available routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/startDate<br/>"
        f"- User must input date formatted as yyyymmdd in place of 'startDate'<br/>"
        f"<br/>"
        f"/api/v1.0/startDate/endDate<br/>"
        f"- User must input dates formatted as yyyymmdd in place of 'startDate' and 'endDate'"
    )

# PRECIPITATION ROUTE
@climateApp.route("/api/v1.0/precipitation")
def precipiation():
    # create session from python to database
    session = Session(engine)
    
    """Return .json of dates and precipitation amounts"""
    # query all dates & precipitation amounts
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    # create a dictionary from the row data and append it to a list
    precipByDate = []
    for date, prcp in results:
        precipDict = {}
        precipDict["Date"] = date
        precipDict["Precipitation"] = prcp
        precipByDate.append(precipDict)
    
    # return results as json
    return jsonify(precipByDate)

# STATIONS ROUTE
@climateApp.route("/api/v1.0/stations")
def stations():
    # create session from python to database
    session = Session(engine)
    
    """Return .json of stations"""
    # query all stations
    results = session.query(Station.station).all()
    
    session.close()
    
    # convert list of tuples into normal list
    allStations = list(np.ravel(results))
   
    # return results as json
    return jsonify(allStations)

# START DATE ONLY ROUTE
@climateApp.route("/api/v1.0/<startDate>")
def startOnly(startDate):
    """Fetch data on the min, max, and average temperature for all dates since startDate."""

    # parse user input into datetime object
    parsedStart = dt.strptime(startDate, "%Y%m%d")
    
    # create session from python to database
    session = Session(engine)
    
    # create list of values to select
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    
    results = session.query(*sel).filter(Measurement.date >= parsedStart).all()
    
    session.close()
    
    # create a dictionary from the data and append it to a list
    startDateSummary = []
    for minTemp, maxTemp, avgTemp in results:
        tempDict = {}
        tempDict["Minimum Temperature"] = minTemp
        tempDict["Maximum Temperature"] = maxTemp
        tempDict["Average Temperature"] = avgTemp
        startDateSummary.append(tempDict)
        
    return jsonify(startDateSummary)

# START TO END DATE ROUTE
@climateApp.route("/api/v1.0/<startDate>/<endDate>")
def startToEnd(startDate, endDate):
    """Fetch data on the min, max, and average temperature for all dates between startDate and endDate."""

    # parse user input into datetime object
    parsedStart = dt.strptime(startDate, "%Y%m%d")
    parsedEnd = dt.strptime(endDate, "%Y%m%d")
    
    # create session from python to database
    session = Session(engine)
    
    # create list of values to select
    sel = [func.min(Measurement.tobs),
           func.max(Measurement.tobs),
           func.avg(Measurement.tobs)]
    
    results = session.query(*sel).filter(Measurement.date >= parsedStart).filter(Measurement.date <= parsedEnd).all()
    
    session.close()
    
    # create a dictionary from the data and append it to a list
    startToEndSummary = []
    for minTemp, maxTemp, avgTemp in results:
        tempDict = {}
        tempDict["Minimum Temperature"] = minTemp
        tempDict["Maximum Temperature"] = maxTemp
        tempDict["Average Temperature"] = avgTemp
        startToEndSummary.append(tempDict)
        
    return jsonify(startToEndSummary)
    
# code to run app
if __name__ == "__main__":
    climateApp.run(debug = True)