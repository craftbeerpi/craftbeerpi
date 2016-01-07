from subprocess import Popen, PIPE, call
from brewapp import app, db, socketio
from model import *
from thread import start_new_thread
import time
from datetime import datetime, timedelta
from brewapp.base.util import *

@brewjob(key="steps")
def stepjob():
    i = 0
    while app.brewapp_jobstate["steps"]:
        #current_step = Step.query.filter_by(state='A').first()
        cs = app.brewapp_current_step;
        #ct = app.brewapp_temperature.get("value1", -1)
        try:
            ct = app.brewapp_kettle_temps[cs.get("kettleid")][1]
        except:
            ct = 0

        if(cs != None):

            if(cs.get("timer") > 0 and cs.get("timer_start") == None and ct >= cs.get("temp")):
                print "START TIMER"
                s = Step.query.get(cs.get("id"))
                #socketio.emit('alert', "", namespace ='/brew')
                s.timer_start = datetime.utcnow()
                app.brewapp_current_step = s.to_json()
                db.session.add(s)
                db.session.commit()
                init()

            if(cs.get("type") == 'A' and cs.get("timer_start") != None):

                # check if timer elapsed
                end = cs.get("timer_start") + cs.get("timer")*60000
                now = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
                #print dict(now)
                if(end < now):
                    print "####NEXT STEP"
                    nextStep()

        else:
            #app.brewapp_current_step = None
            pass
        time.sleep( 1)

@brewinit()
def init():
    app.brewapp_steps = getAsArray(Step, Step.order)
    s = Step.query.filter_by(state='A').first()
    if(s != None):
        app.brewapp_current_step = s.to_json()
    socketio.emit('steps', app.brewapp_steps, namespace ='/brew')

def resetSteps():
    db.session.query(Step).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    init()

def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        setTargetTemp(active.kettleid, 0)
        db.session.add(active)
        db.session.commit()

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        setTargetTemp(inactive.kettleid, inactive.temp)
        db.session.add(inactive)
        db.session.commit()
    init()
