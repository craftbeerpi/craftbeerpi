from flask import Blueprint, render_template, jsonify, request
from flask import make_response
from util import *
from model import *
import time
from brewapp import app, socketio
from views import base
import StringIO
import csv
import datetime

from brewapp import manager
from brewapp.base.automatic.automaticlogic import *
from brewapp.base.hardwareswitch import *

## Returns the all current kettle configs
@app.route('/api/kettle/state', methods=['GET'])
def Kettlestate():
    return  json.dumps(app.brewapp_kettle_state)

## Returns all available thermometer sensors by name
@app.route('/api/kettle/thermometer', methods=['GET'])
def kettleGetW1Thermometer():
    return  json.dumps(app.brewapp_thermometer.getSensors())

## Returns all devices i.e. GPIO1 - GPIO 27
@app.route('/api/kettle/devices', methods=['GET'])
def kettleDevices():
    return  json.dumps(app.brewapp_hardware.getDevices())

## Returns all chart data for a particular kettle
@app.route('/api/kettle/chart/<vid>', methods=['GET'])
def kettlegetChart(vid):
    arr = {}
    arr["temp"] = app.brewapp_kettle_temps_log[int(vid)]
    arr["target"] = app.brewapp_kettle_target_temps_log[int(vid)]
    return  json.dumps(arr)

@app.route('/api/kettle/export/csv/<vid>')
def export(vid):
        si = StringIO.StringIO()
        cw = csv.writer(si)
        k = Kettle.query.get(int(vid))
        r = []
        for d in app.brewapp_kettle_temps_log[int(vid)]:
            r.append([datetime.fromtimestamp((d[0]/ 1000)).strftime('%Y-%m-%d %H:%M:%S'),d[1]])

        cw.writerow(["Time", "Temperature"])
        cw.writerows(r)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=%s.csv" % (k.name)
        output.headers["Content-type"] = "text/csv"
        return output

## Delete all log data
@app.route('/api/kettle/clear', methods=['POST'])
def clearTempLog():
    app.logger.info("Delete all log data")
    kettles = Kettle.query.all()
    for v in kettles:
        app.brewapp_kettle_temps_log[v.id] = []
        app.brewapp_kettle_target_temps_log[v.id] = []
    return ('',204)

## WebSocket METHODS
@socketio.on('switch_automatic', namespace='/brew')
def ws_switch_automatic(data):
    vid = data["vid"]
    if(app.brewapp_kettle_state[vid]["automatic"] == True):
        app.brewapp_kettle_state[vid]["automatic"] = False
        stopPID(vid)
    else:
        app.brewapp_kettle_state[vid]["automatic"]= True
        startAutomatic(vid)
    socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')

@socketio.on('kettle_set_target_temp', namespace='/brew')
def ws_kettle_set_target_temp(data):
    vid = data["kettleid"]
    temp = int(data["temp"])
    setTargetTemp(vid,temp)

def setTargetTemp(vid, temp):
    kettle = Kettle.query.get(vid)
    if(kettle != None):
        kettle.target_temp = temp
        db.session.add(kettle)
        db.session.commit()
        app.brewapp_kettle_state[vid]["target_temp"] = temp
        socketio.emit('kettle_update', getAsArray(Kettle), namespace ='/brew')

def post_post(result=None, **kw):
    result["automatic"] = json.loads(result["automatic"])
    if(result != None):
        print "INIT KETTEL"
        initKettle()
        initHardware()

def pre_post(data, **kw):
    data["automatic"] = json.dumps(data.get("automatic", None))

def post_get_many(result, **kw):
    for o in result["objects"]:
        o["automatic"] = json.loads(o["automatic"])

def post_get_single(result, **kw):
    result["automatic"] = json.loads(result["automatic"])

def post_delete(**kw):
    initKettle();


## INIT
@brewinit()
def init():
    app.brewapp_target_temp_method = setTargetTemp
    manager.create_api(Kettle, methods=['GET', 'POST', 'DELETE', 'PUT'],
    postprocessors={
    'POST': [post_post],
    'PATCH_SINGLE': [post_post],
    'GET_MANY':[post_get_many],
    'DELETE_SINGLE' : [post_delete],
    'GET_SINGLE':[post_get_single]},
    preprocessors={
    'POST':[pre_post],
    'PATCH_SINGLE': [pre_post]})
    initKettle()

def initKettle():
    kettles = Kettle.query.all()
    app.brewapp_kettle_state = {}
    for v in kettles:
        app.brewapp_kettle_temps_log[v.id] = []
        app.brewapp_kettle_target_temps_log[v.id] = []
        app.brewapp_kettle_state[v.id] = {}
        app.brewapp_kettle_state[v.id]["temp"] = 0
        app.brewapp_kettle_state[v.id]["target_temp"] = v.target_temp
        app.brewapp_kettle_state[v.id]["sensorid"]  = v.sensorid
        app.brewapp_kettle_state[v.id]["sensoroffset"]  = v.sensoroffset
        app.brewapp_kettle_state[v.id]["automatic"] =  False
        app.brewapp_kettle_state[v.id]["agitator"]  = v.agitator
        app.brewapp_kettle_state[v.id]["heater"]    = v.heater


## JOBS
@brewjob(key="readtemp", interval=5)
def readKettleTemp():
    for vid in app.brewapp_kettle_state:


        temp = app.brewapp_thermometer.readTemp(app.brewapp_kettle_state[vid]["sensorid"])

        if(app.brewapp_config.get("UNIT", "C") == "F"):
            temp = float(format(9.0/5.0 * temp + 32, '.2f'))
        if(app.brewapp_kettle_state[vid]["sensoroffset"] != None):
            app.brewapp_kettle_state[vid]["temp"] = float(format(temp + app.brewapp_kettle_state[vid]["sensoroffset"], '.2f'))
        else:
            app.brewapp_kettle_state[vid]["temp"] = float(format(temp, '.2f'))

        timestamp = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        app.brewapp_kettle_temps_log[vid] += [[timestamp, app.brewapp_kettle_state[vid]["temp"] ]]
        app.brewapp_kettle_target_temps_log[vid] += [[timestamp, app.brewapp_kettle_state[vid]["target_temp"]]]
    socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')
