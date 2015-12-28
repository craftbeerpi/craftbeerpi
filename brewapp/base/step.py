from subprocess import Popen, PIPE, call
from brewapp import app, db, socketio, brewjob
from model import *
from thread import start_new_thread
import time
from thermometer import tempData1Wire
from datetime import datetime, timedelta

@brewjob(key="steps")
def stepjob():
    i = 0
    while app.brewapp_jobstate["steps"]:

        #current_step = Step.query.filter_by(state='A').first()
        cs = app.brewapp_current_step;
        ct = app.brewapp_temperature.get("value1", -1)

        if(cs != None):
            print cs
            if(cs.get("timer") > 0 and cs.get("timer_start") == None and ct >= cs.get("temp")):
                print "START TIMER"
                #socketio.emit('alert', "", namespace ='/brew')
            #    current_step.timer_start = datetime.utcnow()
            #    db.session.add(current_step)
            #    db.session.commit()
                #socketio.emit('steps', getAsArray(Step), namespace ='/brew')

            if(cs.get("type") == 'A' and cs.get("timer_start") != None):
                print "Next Step"
                # check if timer elapsed
            #    end = current_step.timer_start + timedelta(minutes=current_step.timer)
            #    now = datetime.utcnow()
            #    if(end < now):
            #        print "NEXT STEP"
                    #socketio.emit('steps', getAsArray(Step), namespace ='/brew')
            #        nextStep()
            pass
        else:
            #app.brewapp_current_step = None
            pass
        time.sleep( 1)
