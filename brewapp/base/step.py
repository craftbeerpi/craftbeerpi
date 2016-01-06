import config
import model
from brewapp import manager
from util import brewinit
from model import *
from util import *
from views import base
from brewapp import app, socketio
import time

from flask.ext.restless.helpers import to_dict


@socketio.on('next', namespace='/brew')
@socketio.on('start', namespace='/brew')
def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        setTargetTemp(active.vesselid, 0)
        db.session.add(active)
        db.session.commit()
        app.brewapp_current_step  = None

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        setTargetTemp(inactive.vesselid, inactive.temp)
        db.session.add(inactive)
        db.session.commit()
        app.brewapp_current_step  = to_dict(inactive)
        if(inactive.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((inactive.timer_start - datetime(1970,1,1)).total_seconds())*1000

    socketio.emit('step_update', getAsArray(Step), namespace ='/brew')


## WebSocket
@socketio.on('reset', namespace='/brew')
def ws_reset():
    app.brewapp_current_step  = None
    resetSteps()

## Methods
def resetSteps():
    db.session.query(Step).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    socketio.emit('step_update', getAsArray(Step), namespace ='/brew')

## REST POST PROCESSORS
def post_patch_many(**kw):
    pass
    #init()

def post_get(result=None,**kw):
    ## SORT RESULT BY FIELD 'ORDER'
    result["objects"] = sorted(result["objects"], key=lambda k: k['order'])

@brewinit()
def init():
    ## REST API FOR STEP
    manager.create_api(Step, methods=['GET', 'POST', 'DELETE', 'PUT'],allow_patch_many=True, postprocessors={'PATCH_SINGLE': [post_patch_many], 'DELETE_SINGLE': [post_patch_many], 'POST': [post_patch_many],'GET_MANY': [post_get]})
    s = Step.query.filter_by(state='A').first()
    if(s != None):
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000


@brewjob(key="stepjob", interval=1)
def stepjob():

    if(app.brewapp_current_step == None):
        return

    cs = app.brewapp_current_step;
    #ct = app.brewapp_temperature.get("value1", -1)
    try:
        ct = app.brewapp_vessel_temps[cs.get("vesselid")][1]
    except:
        ct = 0

    if(cs.get("timer") > 0 and cs.get("timer_start") == None and ct >= cs.get("temp")):
        print "START TIMER"
        s = Step.query.get(cs.get("id"))
        s.timer_start = datetime.utcnow()
        app.brewapp_current_step = to_dict(s)
        if(s.timer_start != None):
            app.brewapp_current_step["endunix"] =  int((s.timer_start - datetime(1970,1,1)).total_seconds())*1000
        db.session.add(s)
        db.session.commit()

    if(cs.get("type") == 'A' and cs.get("timer_start") != None):

        # check if timer elapsed

        end = cs.get("endunix") + cs.get("timer")*60000
        now = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
        #print dict(now)
        if(end < now):
            print "####NEXT STEP"
            nextStep()
