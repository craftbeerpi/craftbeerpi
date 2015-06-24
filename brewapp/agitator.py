from brewapp import app, socketio
from flask import render_template
from brewapp.views import addMessage
import json
from brewapp.model import db, Step, Temperatur, Log
import globalprops

PIN = globalprops.agitator_pin

try:
    print "SET GPIO AGITATOR"
    import RPi.GPIO as GPIO # Import GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    globalprops.gpioMode = True
    print "AGITATOR GPIO OK"
except ImportError:
    print "AGITATOR GPIO ERROR"
    globalprops.gpioMode = False

def setAgitator(state):
    # do nothing if state is already set
    if(state == globalprops.agitatorState):
        return
    globalprops.agitatorState = state
    socketio.emit('agitatorupdate', globalprops.agitatorState, namespace ='/brew')
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.agitatorState)

## HTTP Endpoints for agitator
@app.route("/agitator")
def agitatorBase():
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/on")
def agitatorON():
    setAgitator(True)
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/off")
def agitatorOFF():
    setAgitator(False)
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/toggle")
def agitatorTOGGLE():
    if(globalprops.agitatorState):
        setAgitator(False)
    else:
        setAgitator(True)
    return json.dumps({"state": globalprops.agitatorState})

## WebSocket Endpoints for agiator
@socketio.on('agitator', namespace='/brew')
def ws_agitator():
    if(globalprops.agitatorState):
        setAgitator(False)
        addMessage("Ruehrwerk aus")
    else:
        setAgitator(True)
        addMessage("Ruehrwerk ein")
    
