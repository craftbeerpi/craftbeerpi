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


@app.route("/heating")
def heatingBase():
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/on")
def heatingON():
    globalprops.heatingState = True
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.heatingState)
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/off")
def heatingOFF():
    globalprops.heatingState = False
    if(globalprops.gpioMode):
        GPIO.output(PIN, globalprops.heatingState)
    return json.dumps({"state": globalprops.heatingState})

@app.route("/heating/toggle")
def heatingTOGGLE():
    if(globalprops.heatingState):
        globalprops.heatingState = False
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.heatingState)
    else:
        globalprops.heatingState = True
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.heatingState)
    return json.dumps({"state": globalprops.heatingState})

@socketio.on('heating', namespace='/brew')
def ws_heating():
    if(globalprops.heatingState):
        globalprops.heatingState = False
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.heatingState)
        addMessage("Heizung aus")
    else:
        globalprops.heatingState = True
        if(globalprops.gpioMode):
            GPIO.output(PIN, globalprops.heatingState)
        addMessage("Heizung ein")
    socketio.emit('heatingupdate', globalprops.heatingState, namespace ='/brew')
