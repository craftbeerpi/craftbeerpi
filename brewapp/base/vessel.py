from flask import Blueprint, render_template, jsonify, request
from util import *
from model import *
import time
from brewapp import app, socketio
from views import base
from w1_thermometer import *
from brewapp import manager


## HTTP METHODS
@base.route('/gpio', methods=['PUT'])
def updateState():
    data = request.get_json()
    vesselid = data["vid"]
    element = data["element"]
    state = data["state"]
    app.brewapp_vessel_state[vesselid][element]["state"] = state
    return ('', 204)

@app.route('/api/vessel2/state', methods=['GET'])
def vessel2state():
    return  json.dumps(app.brewapp_vessel_state)

@app.route('/api/vessel2/thermometer', methods=['GET'])
def vesselGetW1Thermometer():
    return  json.dumps(getW1Thermometer())

@app.route('/api/vessel2/chart/<vid>', methods=['GET'])
def vesselgetChart(vid):
    return  json.dumps(app.brewapp_vessel_temps_log[int(vid)])

## WebSocket METHODS

@socketio.on('switch_gipo', namespace='/brew')
def ws_switch_gipo(data):
    vesselid = data["vid"]
    element = data["element"]
    if(app.brewapp_vessel_state[vesselid][element]["state"] == True):
        print "SWITCH OFF"
        app.brewapp_vessel_state[vesselid][element]["state"] = False
    else:
        print "SWITCH ON"
        app.brewapp_vessel_state[vesselid][element]["state"] = True

    print app.brewapp_vessel_state
    socketio.emit('vessel_state_update', app.brewapp_vessel_state, namespace ='/brew')

@socketio.on('vessel_set_target_temp', namespace='/brew')
def ws_vessel_set_target_temp(data):
    vid = data["vesselid"]
    temp = int(data["temp"])
    setTargetTemp(vid,temp)


def setTargetTemp(vid, temp):
    vessel = Vessel2.query.get(vid)
    if(vessel != None):
        vessel.target_temp = temp
        db.session.add(vessel)
        db.session.commit()
        socketio.emit('vessel_update', getAsArray(Vessel2), namespace ='/brew')

def post_post(result=None, **kw):
    if(result != None):
        vid = result["id"]
        app.brewapp_vessel_state[vid] = {}
        app.brewapp_vessel_state[vid]["temp"] = 0
        app.brewapp_vessel_state[vid]["sensorid"]  = result["sensorid"]
        app.brewapp_vessel_state[vid]["automatic"] = {"state": False }
        app.brewapp_vessel_state[vid]["agitator"]  = {"state": False, "gpio": result["agitator"]}
        app.brewapp_vessel_state[vid]["heater"]    = {"state": False, "gpio": result["heater"]}

## INIT
@brewinit()
def init():
    app.brewapp_target_temp_method = setTargetTemp
    manager.create_api(Vessel2, methods=['GET', 'POST', 'DELETE', 'PUT'], postprocessors={'POST': [post_post]})
    vessels = Vessel2.query.all()
    for v in vessels:
        app.brewapp_vessel_temps_log[v.id] = []
        app.brewapp_vessel_state[v.id] = {}
        app.brewapp_vessel_state[v.id]["temp"] = 0
        app.brewapp_vessel_state[v.id]["sensorid"]  = v.sensorid
        app.brewapp_vessel_state[v.id]["automatic"] = {"state": False }
        app.brewapp_vessel_state[v.id]["agitator"]  = {"state": False, "gpio": v.agitator}
        app.brewapp_vessel_state[v.id]["heater"]    = {"state": False, "gpio": v.heater}
    print app.brewapp_vessel_state


## JOBS
@brewjob(key="vesseljob3", interval=1)
def vesseljob3():
    for vid in app.brewapp_vessel_state:
        pass
        #print app.brewapp_vessel_state[vid]

@brewjob(key="readtemp", interval=5)
def vesseljob2():
    for vid in app.brewapp_vessel_state:
        app.brewapp_vessel_state[vid]["temp"] = tempData1Wire(app.brewapp_vessel_state[vid]["sensorid"])
        timestamp = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        app.brewapp_vessel_temps_log[vid] += [[timestamp, app.brewapp_vessel_state[vid]["temp"] ]]

        socketio.emit('vessel_state_update', app.brewapp_vessel_state, namespace ='/brew')
