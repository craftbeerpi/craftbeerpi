from brewapp import app, socketio, db
import time
from thread import start_new_thread
from util import *

class PIDBase(object):

    def isRunning(self):
        key = str(self.kid)+"pid"
        return app.brewapp_kettle_automatic[key]

    def getCurrentTemp(self):
        return app.brewapp_kettle_state[self.kid]["temp"]

    def getTargetTemp(self):
        return app.brewapp_kettle_state[self.kid]["target_temp"]

    def switchHeaterON(self):
        app.brewapp_hardware.switchON(app.brewapp_kettle_state[self.kid]["heater"]["gpio"])
        app.brewapp_kettle_state[self.kid]["heater"]["state"] = True
        socketio.emit('kettle_automatic_on', self.kid, namespace ='/brew')

    def switchHeaterOFF(self):
        app.brewapp_hardware.switchOFF(app.brewapp_kettle_state[self.kid]["heater"]["gpio"])
        app.brewapp_kettle_state[self.kid]["heater"]["state"] = False
        socketio.emit('kettle_automatic_off', self.kid, namespace ='/brew')
        
    def __init__(self, kid):
        self.kid = kid

    def pid(self):
        pass



## STOP PID Controller
def stopPID(kid):
    key = str(kid)+"pid";
    app.brewapp_kettle_automatic[key] = False

## START PID Controller
def startPID(kid):
    key = str(kid)+"pid"
    app.brewapp_kettle_automatic[key] = True
    start_new_thread(pidWrapper,(kid,))

def pidWrapper(kid):
    p = app.brewapp_pid_logic(kid)
    p.run()
