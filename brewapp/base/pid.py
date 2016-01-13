import time
from thread import start_new_thread
from brewapp import app, socketio, db
from gpio import *

## STOP PID Controller
def stopPID(vid):
    key = str(vid)+"pid";
    app.brewapp_kettle_automatic[key] = False

## START PID Controller
def startPID(vid):
    key = str(vid)+"pid"
    app.brewapp_kettle_automatic[key] = True
    start_new_thread(pidjob,(vid,))

def getCurrentTemp(kid):
    return app.brewapp_kettle_state[kid]["temp"]

def getTargetTemp(kid):
    return app.brewapp_kettle_state[kid]["target_temp"]

def switchHeaterON(kid):
    switchON(app.brewapp_kettle_state[kid]["heater"]["gpio"])
    app.brewapp_kettle_state[kid]["heater"]["state"] = True

def switchHeaterOFF(kid):
    switchOFF(app.brewapp_kettle_state[kid]["heater"]["gpio"])
    app.brewapp_kettle_state[kid]["heater"]["state"] = False

def isRunning(kid):
    key = str(kid)+"pid"
    return app.brewapp_kettle_automatic[key]

## PID LOGIC IT SELF
## Place your custom code into the while loop

def pidjob(kid):
    app.logger.info("Start PID - Kettle Id: "+ str(kid))
    while isRunning(kid):
        ## Current temperature
        currentTemp =  getCurrentTemp(kid)
        ## Target Temperature
        targetTemp = getTargetTemp(kid)

    
        ## Current Temp is below Target Temp ... switch heater on
        if(currentTemp < targetTemp and app.brewapp_pid_state.get(kid, False) == False):
            app.brewapp_pid_state[kid] = True
            switchHeaterON(kid)
            socketio.emit('kettle_automatic_on', kid, namespace ='/brew')
        ## Current Temp is equal or higher than Target Temp ... switch Heater off
        if(currentTemp >= targetTemp and app.brewapp_pid_state.get(kid, False) == True):
            app.brewapp_pid_state[kid] = False
            switchHeaterOFF(kid)
            socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
        time.sleep(1)

    app.brewapp_pid_state[kid] = False
    switchOFF(kid)
    socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
    app.logger.info("Stop PID - Kettle Id: "+ str(kid))
