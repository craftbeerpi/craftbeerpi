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

## HTTP Endpoints for agitator
@app.route("/agitator")
def agitatorBase():
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/on")
def agitatorON():
    globalprops.agitatorState = True
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.agitatorState)
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/off")
def agitatorOFF():
    globalprops.agitatorState = False
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.agitatorState)
    return json.dumps({"state": globalprops.agitatorState})

@app.route("/agitator/toggle")
def agitatorTOGGLE():
    if(globalprops.agitatorState):
        globalprops.agitatorState = False
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.agitatorState)
    else:
        globalprops.agitatorState = True
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.agitatorState)
    return json.dumps({"state": globalprops.agitatorState})

## WebSocket Endpoints for agiator
@socketio.on('agitator', namespace='/brew')
def ws_agitator():
    if(globalprops.agitatorState):
        globalprops.agitatorState = False
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.agitatorState)
        addMessage("Ruehrwerk aus")
    else:
        globalprops.agitatorState = True
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.agitatorState)
        addMessage("Ruehrwerk ein")
    socketio.emit('agitatorupdate', globalprops.agitatorState, namespace ='/brew')
