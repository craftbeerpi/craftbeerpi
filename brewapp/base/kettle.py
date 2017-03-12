from util import *
from model import *
from brewapp import app, socketio
from brewapp import manager
from brewapp.base.automatic.automaticlogic import *
from flask import send_from_directory

## Returns the all current kettle configs
@app.route('/api/kettle/state', methods=['GET'])
def Kettlestate():
    return  json.dumps(app.brewapp_kettle_state)

@app.route('/api/kettle/<id>/automatic', methods=['POST'])
def switch_automatic(id):
    id = int(id)
    if(app.brewapp_kettle_state[id]["automatic"] == True):
        app.brewapp_kettle_state[id]["automatic"] = False
        stopPID(id)
    else:
        app.brewapp_kettle_state[id]["automatic"]= True
        startAutomatic(id)
    socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')
    return ('',204)

@app.route('/api/kettle/<id>/targettemp', methods=['POST'])
def setTargetTemp(id):
    id = int(id)
    data =request.get_json()
    temp = int(data["temp"])
    setTargetTemp(id,temp)
    return ('',204)

@socketio.on('kettle_set_target_temp', namespace='/brew')
def ws_kettle_set_target_temp(data):
    vid = data["kettleid"]
    temp = int(data["temp"])
    setTargetTemp(vid,temp)

def setTargetTemp(id, temp):
    kettle = Kettle.query.get(id)
    if(kettle != None):
        kettle.target_temp = temp
        db.session.add(kettle)
        db.session.commit()
        app.brewapp_kettle_state[id]["target_temp"] = temp
        socketio.emit('kettle_update', getAsArray(Kettle), namespace ='/brew')

def post_post(result=None, **kw):
    result["automatic"] = json.loads(result["automatic"])
    if(result != None):
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
def initKettle():

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
    app.brewapp_kettle_target_temps_log = {}
    for v in kettles:

        app.brewapp_kettle_state[v.id] = {
            "name": v.name,
            "target_temp": v.target_temp,
            "sensorid": v.sensorid,
            "heater": v.heater,
            "agitator": v.agitator,
            "automatic": False,
        }

@brewjob(key="kettle", interval=5)
def kettlejob():

    for id in app.brewapp_kettle_state:
        k = app.brewapp_kettle_state[id]
        if k["sensorid"] is None or k["sensorid"] == "":
            continue
        temp = app.brewapp_thermometer_last.get(int(k["sensorid"]),0)
        timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
        writeTempToFile("K_" + str(id), timestamp, temp, k["target_temp"])
