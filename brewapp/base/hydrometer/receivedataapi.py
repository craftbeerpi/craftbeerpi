import os
import StringIO
import csv
import datetime
from brewapp import app, socketio, manager
from flask import make_response, send_from_directory, request
from brewapp.base.actor import *
import math

def getOrNewHydrometerId(name):
    row = Hydrometer.query.filter_by(name=name).first()


    if row is None:
        h = Hydrometer(name=name, tuning="-0.003335787*tilt*tilt+ 0.835971079*tilt-20.57776766")
        db.session.add(h)
        db.session.commit()
        app.brewapp_hydrometer_cfg[h.id] = to_dict(h)
        return h.id
    else:
        return row.id

@brewinit()
def init():
    hydrometers = Hydrometer.query.all()
    state_data = {"temp": None, "timestamp": None, "wort": None, "battery": None}
    for row in hydrometers:
        data = to_dict(row)
        app.brewapp_hydrometer_cfg[data["id"]] = data
        app.brewapp_hydrometer_cfg[data["id"]].update(state_data)
        app.brewapp_hydrometer_temps[data["id"]] = {}

## NEW DATA
def calc_wort(polynom, tilt):
    ### here the wort needs to be calculated

    result =  eval(polynom)
    result = round(result,2)
    return result


@app.route('/api/hydrometer/v1/data', methods=['POST'])
def receive_spindle_data():


    data = request.get_json()
    id = getOrNewHydrometerId(data["name"])
    wort = calc_wort(app.brewapp_hydrometer_cfg[id]["tuning"], data["angle"])
    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000

    app.brewapp_hydrometer_cfg[id].update({"temp": data["temperature"], "timestamp": timestamp, "wort": wort})
    app.brewapp_hydrometer_temps[id] = {"temp": data["temperature"], "timestamp": timestamp, "wort": wort}
    writeSpindle("S_"+str(id), timestamp, data["temperature"], wort, data["battery"])

    socketio.emit('hydrometer_update', app.brewapp_hydrometer_cfg, namespace='/brew')
    return ('', 204)

