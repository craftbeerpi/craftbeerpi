import time
from thread import start_new_thread
from brewapp import app, socketio, db
from gpio import *

def stopPID(vid):
    key = str(vid)+"pid";
    app.brewapp_kettle_automatic[key] = False

def startPID(vid):
    key = str(vid)+"pid";
    app.brewapp_kettle_automatic[key] = True
    start_new_thread(pidjob,(vid,))

def pidjob(vid):
    app.logger.info("Start PID - Kettle Id: "+ vid)
    key = str(vid)+"pid";

    while app.brewapp_kettle_automatic[key]:
        ## Current temperature
        ct =  app.brewapp_kettle_state[vid]["temp"]
        ## Target Temperature
        tt = app.brewapp_kettle_state[vid]["target_temp"]
        if(ct < tt and app.brewapp_pid_state.get(vid, False) == False):
            app.brewapp_pid_state[vid] = True
            switchON(app.brewapp_kettle_state[vid]["heater"]["gpio"])
            app.brewapp_kettle_state[vid]["heater"]["state"] = True
            socketio.emit('kettle_automatic_on', vid, namespace ='/brew')
        if(ct >= tt and app.brewapp_pid_state.get(vid, False) == True):
            app.brewapp_pid_state[vid] = False
            switchOFF(app.brewapp_kettle_state[vid]["heater"]["gpio"])
            app.brewapp_kettle_state[vid]["heater"]["state"] = False
            socketio.emit('kettle_automatic_off', vid, namespace ='/brew')
        time.sleep(1)

    app.brewapp_pid_state[vid] = False
    app.logger.info("Stop PID - Kettle Id: "+ vid)
