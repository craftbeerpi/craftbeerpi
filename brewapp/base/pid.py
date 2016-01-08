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
    print "PID START", vid
    key = str(vid)+"pid";
    while app.brewapp_kettle_automatic[key]:
        print "PID"
        ct =  app.brewapp_kettle_state[vid]["temp"]
        print ct
        #tt = app.brewapp_kettle[vid].get("target_temp")
        #if(ct < tt):
        #    switchON(app.brewapp_kettle[vid].get("heater")["gpio"])
    #        app.brewapp_kettle[vid].get("heater")["state"] = True
    #        socketio.emit('kettle_automatic_on', vid, namespace ='/brew')
#
        time.sleep(5)
#        switchOFF(app.brewapp_kettle[vid].get("heater")["gpio"])
#        app.brewapp_kettle[vid].get("heater")["state"] = False
#        socketio.emit('kettle_automatic_off', vid, namespace ='/brew')

    print "PID STOP"
