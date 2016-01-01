import time
from thread import start_new_thread
from brewapp import app, socketio, db
from gpio import *

def stopPID(vid):
    key = str(vid)+"pid";
    app.brewapp_vessel_automatic[key] = False

def startPID(vid):

    key = str(vid)+"pid";
    app.brewapp_vessel_automatic[key] = True
    start_new_thread(pidjob,(vid,))

def pidjob(vid):
    print "PID START"
    key = str(vid)+"pid";
    while app.brewapp_vessel_automatic[key]:
        ct =  app.brewapp_vessel_temps[vid][1]
        tt = app.brewapp_vessel[vid].get("target_temp")
        if(ct < tt):
            switchON(app.brewapp_vessel[vid].get("heater")["gpio"])
            app.brewapp_vessel[vid].get("heater")["state"] = True
            socketio.emit('vessel_automatic_on', vid, namespace ='/brew')

        time.sleep(5)
        switchOFF(app.brewapp_vessel[vid].get("heater")["gpio"])
        app.brewapp_vessel[vid].get("heater")["state"] = False
        socketio.emit('vessel_automatic_off', vid, namespace ='/brew')

    print "PID STOP"
