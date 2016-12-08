import os
import StringIO
import csv
import datetime
from brewapp import app, socketio, manager
from flask import make_response, send_from_directory, request
from brewapp.base.actor import *

@app.route('/api/hydrometer/temps', methods=['GET'])
def getHydrometerTemps():
    return json.dumps(app.brewapp_hydrometer_cfg)

@app.route('/api/hydrometer/', methods=['GET'])
def getHydrometer():
    return json.dumps(app.brewapp_hydrometer_cfg)

@app.route('/api/hydrometer/<id>', methods=['GET'])
def getOneHydrometer(id):
    result = app.brewapp_hydrometer_cfg.get(int(id), None)
    if result is not None:
        return json.dumps(result)
    else:
        return ('', 404)

@app.route('/api/hydrometer/<id>', methods=['POST'])
def updateHydrometer(id):
    app.brewapp_hydrometer_cfg[int(id)] = updateModel(Hydrometer, id, request.get_json())
    return json.dumps(app.brewapp_hydrometer_cfg[int(id)])

@app.route('/api/hydrometer/', methods=['PUT'])
def addHydrometer():
    m =  createModel(Hydrometer, request.get_json())
    app.brewapp_hydrometer_cfg[m["id"]] = m
    return json.dumps(app.brewapp_hydrometer_cfg[m["id"]])

@app.route('/api/hydrometer/<id>', methods=['DELETE'])
def deleteHydrometer(id):
    if deleteModel(Hydrometer, id) is True:
        app.brewapp_hydrometer_cfg.pop(int(id), None)
    return ('', 204)