from flask import Flask,jsonify, json, request, send_from_directory
from flask_socketio import SocketIO, emit
import flask_restless
import time
from flask_sqlalchemy import SQLAlchemy
from flask_restless.helpers import to_dict
from model import *
from brewapp import app, socketio, manager
import datetime
from brewapp.base.util import *
from brewapp.base.actor import *


app.cbp['CURRENT_TASK'] = {}
app.cbp['FERMENTERS'] = {}


@brewinit()
def load():
    for s in Fermenter.query.all():
        app.cbp['FERMENTERS'][s.id] = to_dict(s)
    for s in FermenterStep.query.filter_by(state='A').all():
        app.cbp['CURRENT_TASK'][s.fermenter_id] = to_dict(s)
        if s.state == 'A' and s.timer_start is not None:
            app.cbp['CURRENT_TASK'][s.fermenter_id]["endunix"] = int((s.timer_start - datetime.datetime(1970, 1, 1)).total_seconds())

    app.logger.info("CURRENT_TASK")
    app.logger.info(app.cbp['CURRENT_TASK'])



def post_post(result, **kw):
    app.cbp['FERMENTERS'][result["id"]] = result


def post_patch(result, **kw):
    app.cbp['FERMENTERS'][result["id"]].update(result)
    if app.cbp['CURRENT_TASK'].get(result["id"], None) is not None and  app.cbp['CURRENT_TASK'][result["id"]]["id"] == result["id"]:
        for key in ["name", "target_temp"]:
            app.cbp['CURRENT_TASK'][result["id"]][key] = result[key]


def reload_fermenter(id):
    f = Fermenter.query.get(id)
    d = to_dict(f, deep={'steps': []})
    app.cbp['FERMENTERS'][f.id] = d
    socketio.emit('fermenter_update', d, namespace='/brew')




manager.create_api(Fermenter, methods=['GET', 'POST', 'PUT', 'DELETE'],  results_per_page=None, postprocessors={ 'PUT_SINGLE': [post_patch], 'POST': [post_post]})
manager.create_api(FermenterStep, methods=['GET', 'POST', 'PUT', 'DELETE'], results_per_page=None, postprocessors={'PUT_SINGLE': [post_patch]})

@app.route('/api/fermenter/step/order', methods=['POST'])
def fermentation_order_steps():
    data = request.get_json()
    for s in FermenterStep.query.filter_by(fermenter_id=int(data["id"])).order_by(FermenterStep.order).all():
        s.order = data["steps"][str(s.id)];
        db.session.add(s)
        db.session.commit()

    return ('', 204)

@app.route('/api/fermenter/<id>/next', methods=['POST'])
def next(id):

    active = FermenterStep.query.filter_by(fermenter_id=int(id), state='A').first()
    inactive = FermenterStep.query.filter_by(fermenter_id=int(id), state='I').order_by(FermenterStep.order).first()
    if active is not None:
        active.state = "D"
        active.end = datetime.datetime.utcnow()
    if inactive is not None:
        setTargetTemp(int(id), inactive.temp)
        inactive.start = datetime.datetime.utcnow()
        inactive.state = "A"
        app.cbp['CURRENT_TASK'][int(id)]  = to_dict(inactive)
        temp = app.brewapp_thermometer_last[app.cbp['FERMENTERS'][int(id)]["sensorid"]]

        if temp >= inactive.temp:
            app.cbp['CURRENT_TASK'][int(id)]["direction"] = "C"
        else:
            app.cbp['CURRENT_TASK'][int(id)]["direction"] = "H"
    else:
        app.cbp['CURRENT_TASK'].pop(int(id), None)
    db.session.commit()
    reload_fermenter(int(id))
    return ('', 204)

@app.route('/api/fermenter/<id>/start', methods=['POST'])
def start(id):
    return next(id)


@app.route('/api/fermenter/<id>/stop', methods=['POST'])
def stop(id):
    db.session.query(FermenterStep).filter_by(fermenter_id=int(id)).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    app.cbp['CURRENT_TASK'].pop(int(id), None)
    reload_fermenter(int(id))

    return "OK"

@app.route('/reset')
def reset():
    active = FermenterStep.query.filter_by(state='A').first()
    db.session.commit()
    app.cbp['CURRENT_TASK'] = None
    return ('', 204)

@app.route('/api/fermenter/<id>/targettemp', methods=['POST'])
def setTargetTempFermenter(id):
    id = int(id)
    data = request.get_json()
    temp = int(data["temp"])
    setTargetTemp(id, temp)
    return ('', 204)


def setTargetTemp(id, temp):
    fermenter = Fermenter.query.get(id)
    if fermenter is not None:
        fermenter.target_temp = temp
        db.session.commit()
        reload_fermenter(id)


@app.route('/api/fermenter/state', methods=['GET'])
def fermenter_state():
    return json.dumps(app.brewapp_automatic_state)

def hystresis(id):
    while app.brewapp_automatic_state["F" + id]:

        fermenter = app.cbp['FERMENTERS'][int(id)]


        if type(fermenter["sensorid"]) is not int:
            socketio.emit('message', {"headline": "NO_TERMOMETER", "message": "NO_THERMOMETER_DEFINED"}, namespace='/brew')
            break

        temp = app.brewapp_thermometer_last[fermenter["sensorid"]]

        target_temp = fermenter["target_temp"]
        heater_min = fermenter["heateroffset_min"]
        heater_max = fermenter["heateroffset_max"]

        cooler_min = fermenter["cooleroffset_min"]
        cooler_max = fermenter["cooleroffset_max"]

        heater_id = fermenter["heaterid"] if type(fermenter["heaterid"]) is int else None
        cooler_id = fermenter["coolerid"] if type(fermenter["coolerid"]) is int else None


        if heater_id is not None:
            if temp + heater_min < target_temp:
                switchOn(fermenter["heaterid"])

            if temp + heater_max > target_temp:
                switchOff(fermenter["heaterid"])

        if cooler_id is not None:
            if temp > target_temp + cooler_min:
                switchOn(fermenter["coolerid"])

            if temp < target_temp + cooler_max:
                switchOff(fermenter["coolerid"])

        socketio.sleep(1)

    app.brewapp_automatic_state["F" + id] = False

    if type(fermenter["heaterid"]) is int:
        switchOff(fermenter["heaterid"])
    if type(fermenter["coolerid"]) is int:
        switchOff(fermenter["coolerid"])


@app.route('/api/fermenter/<id>/automatic', methods=['POST'])
def fermenter_automatic(id):
    if not app.brewapp_automatic_state.get("F" + id, False):
        app.brewapp_automatic_state["F" + id] = True
        t = socketio.start_background_task(hystresis, id)
    else:
        app.brewapp_automatic_state["F" + id] = False

    socketio.emit('fermenter_state_update', app.brewapp_automatic_state, namespace='/brew')
    return ('', 204)



@brewjob(key="fermenter", interval=60)
def fermenterjob():
    for id in app.brewapp_fermenters:
        fermenter = app.brewapp_fermenters[id]
        temp = app.brewapp_thermometer_last[fermenter["sensorid"]]
        timestamp = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) * 1000
        writeTempToFile("F_" + str(fermenter["id"]), timestamp, temp, fermenter["target_temp"])

@brewjob(key="fermenter_control", interval=0.1)
def step_control():
    for i in app.cbp['CURRENT_TASK']:
        step = app.cbp['CURRENT_TASK'][i]
        fermenter = app.cbp['FERMENTERS'][i]
        temp = app.brewapp_thermometer_last[fermenter["sensorid"]]

        if step.get("timer_start", None) is None:
            if(step.get("direction", "C") == 'C'):
                if temp <= step["temp"] :
                    start_timer(step.get("id"), i)
            else:
                if temp >= step["temp"]:
                    start_timer(step.get("id"), i)

        if (step.get("timer_start") != None):

            end = step.get("endunix") + step.get("days") * 86400  + step.get("hours") * 3600 + step.get("minutes") * 60
            now = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())

            if end < now:
                app.logger.info("Next Step")
                next(step["fermenter_id"])

def start_timer(stepid, fermenter_id):
    app.logger.info("Start Timer")
    d = datetime.datetime.utcnow()
    FermenterStep.query.filter_by(id=stepid).update({'timer_start': d})
    db.session.commit()
    app.cbp['CURRENT_TASK'][fermenter_id]["timer_start"] = d
    app.cbp['CURRENT_TASK'][fermenter_id]["endunix"] = int((d - datetime.datetime(1970, 1, 1)).total_seconds())

    reload_fermenter(fermenter_id)


### Temp Logging


@brewjob(key="fermenter", interval=60)
def fermenterjob():
    for id in app.cbp['FERMENTERS']:
        fermenter = app.cbp['FERMENTERS'][id]
        temp = app.brewapp_thermometer_last[fermenter["sensorid"]]
        timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
        writeTempToFile("F_" + str(fermenter["id"]), timestamp, temp, fermenter["target_temp"])
