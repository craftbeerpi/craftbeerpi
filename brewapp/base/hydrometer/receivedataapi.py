import os
import StringIO
import csv
import datetime
from brewapp import app, socketio, manager
from flask import make_response, send_from_directory, request
from brewapp.base.actor import *


def getOrNewHydrometerId(name):
    row = Hydrometer.query.filter_by(name=name).first()
    if row is None:
        h = Hydrometer(name=name)
        db.session.add(h)
        db.session.commit()
        app.brewapp_hydrometer_cfg[h.id] = to_dict(h)
        return h.id
    else:
        return row.id

@brewinit()
def init():
    hydrometers = Hydrometer.query.all()
    for row in hydrometers:
        data = to_dict(row)
        app.brewapp_hydrometer_cfg[data["id"]] = data
        app.brewapp_hydrometer_temps[data["id"]] = {}

## NEW DATA
def calc_wort(temp, angle):
    ### here the wort needs to be calculated
    pass

@app.route('/api/spindle/data', methods=['POST'])
def receive_spindle_data():

    data = request.get_json()
    id = getOrNewHydrometerId(data["name"])
    wort = calc_wort(data["temperature"], data["angle"])
    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
    app.brewapp_hydrometer_temps[id] = {"temp": data["temperature"], "timestamp": timestamp, "wort": data["angle"]}
    writeSpindle("S_"+str(id), timestamp, data["temperature"], data["angle"], data["battery"])
    return ('', 204)

