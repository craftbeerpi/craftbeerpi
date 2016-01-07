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
    kettleid = data["vid"]
    element = data["element"]
    state = data["state"]
    app.brewapp_kettle_state[kettleid][element]["state"] = state
    return ('', 204)

@app.route('/api/kettle2/state', methods=['GET'])
def kettle2state():
    return  json.dumps(app.brewapp_kettle_state)

@app.route('/api/kettle2/thermometer', methods=['GET'])
def kettleGetW1Thermometer():
    return  json.dumps(getW1Thermometer())

@app.route('/api/kettle2/chart/<vid>', methods=['GET'])
def kettlegetChart(vid):
    return  json.dumps(app.brewapp_kettle_temps_log[int(vid)])

## WebSocket METHODS

@socketio.on('switch_gipo', namespace='/brew')
def ws_switch_gipo(data):
    kettleid = data["vid"]
    element = data["element"]
    if(app.brewapp_kettle_state[kettleid][element]["state"] == True):
        print "SWITCH OFF"
        app.brewapp_kettle_state[kettleid][element]["state"] = False
    else:
        print "SWITCH ON"
        app.brewapp_kettle_state[kettleid][element]["state"] = True

    print app.brewapp_kettle_state
    socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')

@socketio.on('kettle_set_target_temp', namespace='/brew')
def ws_kettle_set_target_temp(data):
    vid = data["kettleid"]
    temp = int(data["temp"])
    setTargetTemp(vid,temp)


def setTargetTemp(vid, temp):
    kettle = Kettle2.query.get(vid)
    if(kettle != None):
        kettle.target_temp = temp
        db.session.add(kettle)
        db.session.commit()
        socketio.emit('kettle_update', getAsArray(Kettle2), namespace ='/brew')

def post_post(result=None, **kw):
    if(result != None):
        vid = result["id"]
        app.brewapp_kettle_state[vid] = {}
        app.brewapp_kettle_state[vid]["temp"] = 0
        app.brewapp_kettle_state[vid]["sensorid"]  = result["sensorid"]
        app.brewapp_kettle_state[vid]["automatic"] = {"state": False }
        app.brewapp_kettle_state[vid]["agitator"]  = {"state": False, "gpio": result["agitator"]}
        app.brewapp_kettle_state[vid]["heater"]    = {"state": False, "gpio": result["heater"]}

## INIT
@brewinit()
def init():
    app.brewapp_target_temp_method = setTargetTemp
    manager.create_api(Kettle2, methods=['GET', 'POST', 'DELETE', 'PUT'], postprocessors={'POST': [post_post]})
    kettles = Kettle2.query.all()
    for v in kettles:
        app.brewapp_kettle_temps_log[v.id] = []
        app.brewapp_kettle_state[v.id] = {}
        app.brewapp_kettle_state[v.id]["temp"] = 0
        app.brewapp_kettle_state[v.id]["sensorid"]  = v.sensorid
        app.brewapp_kettle_state[v.id]["automatic"] = {"state": False }
        app.brewapp_kettle_state[v.id]["agitator"]  = {"state": False, "gpio": v.agitator}
        app.brewapp_kettle_state[v.id]["heater"]    = {"state": False, "gpio": v.heater}
    print app.brewapp_kettle_state


## JOBS
@brewjob(key="kettlejob3", interval=1)
def kettlejob3():
    for vid in app.brewapp_kettle_state:
        pass
        #print app.brewapp_kettle_state[vid]

@brewjob(key="readtemp", interval=5)
def kettlejob2():
    for vid in app.brewapp_kettle_state:
        app.brewapp_kettle_state[vid]["temp"] = tempData1Wire(app.brewapp_kettle_state[vid]["sensorid"])
        timestamp = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        app.brewapp_kettle_temps_log[vid] += [[timestamp, app.brewapp_kettle_state[vid]["temp"] ]]

        socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')
