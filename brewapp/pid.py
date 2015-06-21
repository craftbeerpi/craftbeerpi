from brewapp import app, socketio
from flask import render_template
import json
from brewapp.model import db, Step, Temperatur, Log
import globalprops
from brewapp.views import addMessage

## This file contains all the HTTP and WebSocket Endpoints for PID

@app.route("/pid")
def pidBase():
    return json.dumps({"state": globalprops.pidState})

@app.route("/pid/on")
def pidON():
    globalprops.pidState = True
    return json.dumps({"state": globalprops.pidState})

@app.route("/pid/off")
def pidOFF():
    globalprops.pidState = False
    return json.dumps({"state": globalprops.pidState})

@app.route("/pid/toggle")
def pidTOGGLE():
    if(globalprops.pidState):
        globalprops.pidState = False
    else:
        globalprops.pidState = True
    return json.dumps({"state": globalprops.pidState})

@socketio.on('pid', namespace='/brew')
def ws_pid():
    if(globalprops.pidState):
        globalprops.pidState = False
        addMessage("PID aus")
    else:
        globalprops.pidState = True
        addMessage("PID an")
    socketio.emit('pidupdate', globalprops.pidState, namespace ='/brew')

