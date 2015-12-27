from subprocess import Popen, PIPE, call
from brewapp import app, db, socketio
from model import *
from thread import start_new_thread
import time
from thermometer import tempData1Wire
from datetime import datetime, timedelta

def stepjob():
    i = 0
    while True:
        current_step = Step.query.filter_by(state='A').first()

        if(current_step != None):
            print current_step.temp
            app.brewapp_current_step = current_step.to_json()
            if(current_step.timer > 0 and current_step.timer_start == None and  app.brewapp_temperature.get("value1", -1) >= current_step.temp):
                print "START TIMER"
                #socketio.emit('alert', "", namespace ='/brew')
                current_step.timer_start = datetime.utcnow()
                db.session.add(current_step)
                db.session.commit()
                #socketio.emit('steps', getAsArray(Step), namespace ='/brew')

            if(current_step.type == 'A' and current_step.timer_start != None):
                # check if timer elapsed
                end = current_step.timer_start + timedelta(minutes=current_step.timer)
                now = datetime.utcnow()
                if(end < now):
                    print "NEXT STEP"
                    #socketio.emit('steps', getAsArray(Step), namespace ='/brew')
                    nextStep()
        else:
            app.brewapp_current_step = None
        time.sleep( 1)



def job2():
    start_new_thread(stepjob,())

app.brewapp_jobs.append(job2)
