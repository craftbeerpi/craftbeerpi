import config
import model
from brewapp import manager
from model import *
from util import *
from brewapp import app, socketio
import time
from flask import request
import os
from werkzeug import secure_filename
from views import base
import sqlite3
from datetime import datetime

from buzzer import nextStepBeep, timerBeep, resetBeep
from flask_restless.helpers import to_dict


@app.route('/api/step/order', methods=['POST'])
def order_steps():
    data = request.get_json()

    steps =  Step.query.all()
    for s in steps:
        s.order = data[str(s.id)]
        db.session.add(s)
        db.session.commit()
    return ('',204)

@app.route('/api/step/clear', methods=['POST'])
def getBrews():
    Step.query.delete()
    db.session.commit()
    return ('',204)

@socketio.on('start', namespace='/brew')
def startStep(*kwargs):
    nextStep()

@socketio.on('next', namespace='/brew')
def nextStep2():
    nextStep()

def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(inactive == None):
        socketio.emit('message', {"headline": "BREWING_FINISHED", "message": "BREWING_FINISHED_MESSAGE"}, namespace ='/brew')

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        setTargetTemp(active.kettleid, 0)
        db.session.add(active)
        db.session.commit()
        app.brewapp_current_step  = None

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        setTargetTemp(inactive.kettleid, inactive.temp)
        db.session.add(inactive)
        db.session.commit()
        app.brewapp_current_step  = to_dict(inactive)
        if(inactive.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((inactive.timer_start - datetime(1970,1,1)).total_seconds())*1000

    nextStepBeep()
    socketio.emit('step_update', getSteps(), namespace ='/brew')

## WebSocket
@socketio.on('reset', namespace='/brew')
def reset():
    app.brewapp_current_step  = None
    resetSteps()



## Methods
@socketio.on('reset_current_step', namespace='/brew')
def resetCurrentSteps():
    resetBeep()
    active = Step.query.filter_by(state='A').first()
    active.start = datetime.utcnow()
    active.end = None
    active.timer_start = None
    setTargetTemp(active.kettleid, active.temp)
    app.brewapp_current_step = to_dict(active)
    db.session.add(active)
    db.session.commit()
    socketio.emit('step_update', getSteps(), namespace ='/brew')

@socketio.on('start_timer_current_step', namespace='/brew')
def start_timer_of_current_step():
    resetBeep()
    active = Step.query.filter_by(state='A').first()
    active.timer_start = datetime.utcnow()
    setTargetTemp(active.kettleid, active.temp)
    app.brewapp_current_step = to_dict(active)
    app.brewapp_current_step["endunix"] = int((active.timer_start - datetime(1970, 1, 1)).total_seconds()) * 1000

    db.session.add(active)
    db.session.commit()
    socketio.emit('step_update', getSteps(), namespace ='/brew')

## Methods
def resetSteps():
    resetBeep()
    db.session.query(Step).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    socketio.emit('step_update', getSteps(), namespace ='/brew')

## REST POST PROCESSORS
def post_patch_many(result, **kw):
    pass
    #init()

def pre_put(data, **kw):
    pass

def post_get(result=None,**kw):
    ## SORT RESULT BY FIELD 'ORDER'
    result["objects"] = sorted(result["objects"], key=lambda k: k['order'])

    pass
    '''
    for o in result["objects"]:
        if(o["start"] != None):
            o["start"] = o["start"]  + "+00:00"
        if(o["timer_start"] != None):
            o["timer_start"] = o["timer_start"]  + "+00:00"
        if(o["end"] != None):
            o["end"] = o["end"]  + "+00:00"
    '''

@brewinit()
def init():
    ## REST API FOR STEP
    manager.create_api(Step, methods=['GET', 'POST', 'DELETE', 'PUT'],allow_patch_many=True, results_per_page=None, postprocessors=
    {'GET_MANY': [post_get]})
    s = Step.query.filter_by(state='A').first()
    if(s != None):
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000


@brewjob(key="stepjob", interval=0.1)
def stepjob():


    ## Skip if no step is active
    if(app.brewapp_current_step == None):
        return
    ## current step
    cs = app.brewapp_current_step;
    ## get current temp of target kettle
    try:
        id = int(app.brewapp_kettle_state[cs.get("kettleid")]["sensorid"])
        ct = app.brewapp_thermometer_last[id];
    except:
        ct = 0

    #print cs.get("timer")
    #print cs.get("timer_start")
    #print cs.get("temp")
    #print ct
    ## check if target temp reached and timer can be started
    if(cs.get("timer") is not None and cs.get("timer_start") == None and ct >= cs.get("temp")):

        s = Step.query.get(cs.get("id"))
        s.timer_start = datetime.utcnow()
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000
            timerBeep()
        db.session.add(s)
        db.session.commit()
        socketio.emit('step_update', getSteps(), namespace ='/brew', broadcast=True)


    ## if Automatic step and timer is started
    if(cs.get("timer_start") != None):
        # check if timer elapsed
        end = cs.get("endunix") + cs.get("timer")*60000
        now = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        ## switch to next step if timer is over
        if(end < now ):

            if(cs.get("type") == 'A'):
                nextStep()
            if(cs.get("type") == 'M' and app.brewapp_current_step.get("finished", False) == False):
                nextStepBeep()

                app.brewapp_current_step["finished"] = True

def getSteps():
    steps = getAsArray(Step, order = "order")
    '''
    for o in steps:
        if(o["start"] != None):
            o["start"] = o["start"]  + "+00:00"
        if(o["timer_start"] != None):
            o["timer_start"] = o["timer_start"]  + "+00:00"
        if(o["end"] != None):
            o["end"] = o["end"]  + "+00:00"
    '''
    return steps
