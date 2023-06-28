# Import the dependencies.
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask , jsonify



#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)

#################################################


# Flask Routes
@app.route("/")
def welcome():
    return(f"welcome page <br/>"
           
           f" routes <br/>"
           
           f"/api/v1.0/precipitation <br/>"
           
           f"/api/v1.0/stations <br/>"
           
           f"/api/v1.0/tobs <br/>"
           
           f"/api/v1.0/start/end <br/>"
           
           )       


@app.route("/api/v1.0/precipitation")

def precipitation():
    last_12_months_prcp = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago, Measurement.prcp != None).\
    order_by(Measurement.date).all()
    return jsonify(dict(year_prcp))
    
        
    
@app.route("/api/v1.0/stations")

def station():
    result = session.query(Station.station).all()
    st_list = list(np.ravel(result))
    return jsonify (st_list)



@app.route("/api/v1.0/tobs")

def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)




@app.route ("/api/v1.0/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
            

if __name__ == "__main__":
   app.run(debug=True)
#################################################




