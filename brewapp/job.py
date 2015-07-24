from thread import start_new_thread
from brewapp import app, socketio
from brewapp.model import db, Temperatur
from datetime import datetime, timedelta
import globalprops
import thermometer
from flask.ext.socketio import SocketIO, emit
from brewapp.model import db, Step, Temperatur, Log, Config
import time
from views import getAsArray, nextStep
from pidypi import pidpy
from brewapp.gpio import setState, gpio_state
from Queue import Queue
import json
from random import randint

## GLOBALS

temp_queue = Queue(maxsize=0)

# STEP CONTROL JOB
def stepjob():

    print "START STEP JOB"
    temp_count = 0
    while True:
        current_step = Step.query.filter_by(state='A').first()

        if(current_step != None):
            globalprops.current_step = current_step.to_json()
        else:
            globalprops.current_step = None
            time.sleep(1)
            continue

        update_step = False

        if(current_step != None):
            # Target temp reached! Start Timer

            if(current_step.timer > 0 and current_step.timer_start == None and  globalprops.temps['temp1'][1] >= current_step.temp):
                print "START TIMER"
                current_step.timer_start = datetime.utcnow()
                db.session.add(current_step)
                db.session.commit()
                update_step = True

            if(current_step.type == 'A' and current_step.timer_start != None):
                # check if timer elapsed
                end = current_step.timer_start + timedelta(minutes=current_step.timer)
                now = datetime.utcnow()
                if(end < now):
                    print "NEXT STEP"
                    update_step = True
                    nextStep()

        ## Push steps to connected clients
        if(update_step == True):
            socketio.emit('steps', getAsArray(Step), namespace ='/brew')

        time.sleep( 1 )

import random

## READ TEMP JOB
def tempjob(q):
    print "START TEMP JOB"
    #global current_temp
    while True:
        sensorId1 = Config.getParameter("tempSensorId1", "{\"name\": \"no\"}", True)

        t = Temperatur()
        t.time = datetime.utcnow()

        if(sensorId1["name"] != "no"):
            t.value1 = thermometer.tempData1Wire(sensorId1['id'])
            #t.value2 = random.randint(0,50)
            #t.value3 = random.randint(0,50)
            #t.value4 = random.randint(0,50)
            #t.value5 = random.randint(0,50)

        ## Save temperatur in database
        db.session.add(t)
        db.session.commit()

        globalprops.temps = t.to_json()
        q.put(globalprops.temps)

        time.sleep( Config.getParameter("temp_db_interval", 5) )



def updateChart(queues):
    while True:
        new_data = False
        q = queues['temps']
        update = {}

        while not q.empty():
            t = q.get()

            for x in globalprops.temps.keys():
                if(x is not "temp1"):
                    continue
                update[x] = [[t[x][0], t[x][1]]]

                if(x not in globalprops.chart_cache):
                    globalprops.chart_cache[x] = []
                globalprops.chart_cache[x] += [[t[x][0], t[x][1]]]

            new_data = True
            q.task_done()

        if(new_data == True):
            for k in globalprops.chart_queues.keys():
                if(k != 'temps'):
                    update[k] = getQueueData(queues, k)
            socketio.emit('chart_update', update, namespace ='/brew')

        time.sleep(1)

def getQueueData(queues, name):
    q2 = queues[name]
    result = []
    while not q2.empty():
        entry = q2.get()
        result.append([entry['time'], entry['value']])
        q2.task_done()

    if(len(result) > 0):
        if(name not in globalprops.chart_cache):
            globalprops.chart_cache[name] = []
        globalprops.chart_cache[name] += result
    return result


def heatjob():
    print "START HEAT"
    while True:

        ## PID NOT or no current step ACTIVE SKIP
        if(globalprops.pidState == True and globalprops.current_step != None):
            if(globalprops.temps['temp1'][1] < globalprops.current_step['temp'] and gpio_state['gpio_heat']== False):
                setState("heat", "on", False)
            elif(globalprops.temps['temp1'][1] > globalprops.current_step['temp'] and gpio_state['gpio_heat'] == True):
                setState("heat", "off", False)

        time.sleep(1)


## Start the theads in background
start_new_thread(tempjob,(globalprops.chart_queues['temps'],))
start_new_thread(stepjob,())
start_new_thread(heatjob,())
start_new_thread(updateChart,(globalprops.chart_queues,))
