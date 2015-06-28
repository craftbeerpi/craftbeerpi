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
from brewapp.gpio import setState

#from heating import setHeating
#from agitator import setAgitator

## GLOBALS
#current_temp = 0
target_temp = 0
current_step = None 

# STEP CONTROL JOB
def stepjob():

    print "START STEP JOB"
    
    temp_count = 0
    global temp
    global target_temp
    global current_step
    while True:
        current_step = Step.query.filter_by(state='A').first()

        if(current_step != None):
            target_temp = current_step.temp
        else:
            target_temp = -1;
            time.sleep(1)
            continue
            
        update_step = False

        if(current_step != None):

            pid_agitator  = Config.getParameter("pid_agitator", False)
            ## Switch agiator on for heating phase            
            if(pid_agitator == True and current_step.timer_start == None  and  globalprops.current_temp < current_step.temp and globalprops.pidState == True):
                print "SWITCH ON"
                setState("agitator", "on", False)

            # Target temp reached! Start Timer
            if(current_step.timer > 0 and current_step.timer_start == None and  globalprops.current_temp >= current_step.temp):
                print "START TIMER"
                # stop the agiator if target temp reached
                if(pid_agitator and globalprops.pidState == True):
                    setState("agitator", "off", False)
                
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

## READ TEMP JOB 
def tempjob():
    print "START TEMP JOB"
    #global current_temp
    while True:
        sensorId1 = Config.getParameter("tempSensorId1", "{\"name\": \"no\"}", True)
        sensorId2 = Config.getParameter("tempSensorId2", "{\"name\": \"no\"}", True)
        sensorId3 = Config.getParameter("tempSensorId3", "{\"name\": \"no\"}", True)
        sensorId4 = Config.getParameter("tempSensorId4", "{\"name\": \"no\"}", True)
        sensorId5 = Config.getParameter("tempSensorId5", "{\"name\": \"no\"}", True)
  
        t = Temperatur()
        t.time = datetime.utcnow()
        
        if(sensorId1["name"] != "no"):
            globalprops.current_temp = thermometer.tempData1Wire(sensorId1)
            t.name1 = sensorId1["name"]
            t.value1 = globalprops.current_temp 

        if(sensorId2["name"] != "no"):
            globalprops.current_temp = thermometer.tempData1Wire(sensorId2)
            t.name2 = sensorId2["name"]
            t.value2 = globalprops.current_temp 

        if(sensorId3["name"] != "no"):
            globalprops.current_temp = thermometer.tempData1Wire(sensorId3)
            t.name3 = sensorId3["name"]
            t.value3 = globalprops.current_temp 

        if(sensorId4["name"] != "no"):
            globalprops.current_temp = thermometer.tempData1Wire(sensorId4)
            t.name4 = sensorId4["name"]
            t.value4 = globalprops.current_temp 

        if(sensorId5["name"] != "no"):
            globalprops.current_temp = thermometer.tempData1Wire(sensorId5)
            t.name5 = sensorId5["name"]
            t.value5 = globalprops.current_temp 
        
        ## Save temperatur in database
        db.session.add(t)
        db.session.commit()

        ## Add to cache
        globalprops.temp_cache.append(t.to_json())
    
        ## push temperatur update to all connected clients
        socketio.emit('temp', {'temp': t.value1, 'time': t.to_unixTime(t.time)}, namespace='/brew')
        time.sleep( Config.getParameter("temp_db_interval", 5) )


## PID JOB 
##
def pidjob():
    print "START PID"
    #global current_temp
    global target_temp

    p = Config.getParameter("p", 102)
    i = Config.getParameter("i", 100)
    d = Config.getParameter("d", 5)
    interval = Config.getParameter("pid_interval", 5)


    pid = pidpy(interval,p,i,d)

    while True:
        ## PID NOT or no current step ACTIVE SKIP
        if(globalprops.pidState == False or current_step == None):
            timestamp = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000 
            globalprops.heatLog.append([timestamp,0])
            time.sleep(interval)
            continue

        # hysteresis 
        # if the temp is to below the target temp. heating 100 % on
        # PID Not needed
        #if(current_temp < target_temp - globalprops.hysteresis_min):
        #    setHeating(True)
        #    time.sleep(globalprops.pid_interval)
        #    continue

        ## Calculate heating
        heat_percent = pid.calcPID_reg4(globalprops.current_temp, target_temp, True)
        heating_time = interval * heat_percent / 100
        wait_time = interval - heating_time
   
        ## HEATING ON
        setState("heat", "on", False)
        time.sleep(heating_time)
        ## HEATING OFF
        setState("heat", "off", False)
        time.sleep(wait_time)


## Start the theads in background
start_new_thread(tempjob,())
start_new_thread(stepjob,())
start_new_thread(pidjob,())

