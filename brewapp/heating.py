from brewapp import app, socketio
from flask import render_template
import json
from brewapp.model import db, Step, Temperatur, Log
import globalprops
from brewapp.views import addMessage

PIN = globalprops.heating_pin

try:
    print "SET GPIO HEATING"
    import RPi.GPIO as GPIO # Import GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    globalprops.gpioMode = True
    print "HEATING GPIO OK"
except ImportError:
    print "HEATING GPIO ERROR"
    globalprops.gpioMode = False


def setHeating(state):
    ## do nothing if the state is already set
    if(state == globalprops.heatingState):
        return
    globalprops.heatingState = state
    socketio.emit('heatingupdate', globalprops.heatingState, namespace ='/brew')
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.heatingState)

@app.route("/heating")
def heatingBase():
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/on")
def restHeatingON():
    setHeating(True)
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/off")
def restHeatingOFF():
    setHeating(False)
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/toggle")
def heatingTOGGLE():
    if(globalprops.heatingState):
        setHeating(False)
    else:
        setHeating(True)
    return json.dumps({"state": globalprops.heatingState})

@socketio.on('heating', namespace='/brew')
def ws_heating():
    if(globalprops.heatingState):
        setHeating(False)
        addMessage("Heizung aus")
    else:
        setHeating(True)
        addMessage("Heizung ein")
    


