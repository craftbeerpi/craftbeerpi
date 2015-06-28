from brewapp import app, socketio
from flask import render_template
from flask.ext.socketio import SocketIO, emit
import json
from brewapp.model import db, Step, Temperatur, Log, Config
import globalprops
from datetime import datetime, timedelta
from brewapp.gpio import gpio_state, getAllGPIO


## Index View
@app.route('/')
def index():
    return render_template("index.html" )

## Helper method to transform db model to json
def getAsArray(obj):
    steps=obj.query.all()
    ar = []
    for t in steps:
        ar.append(t.to_json())
    return ar

## Helpr method to start the next step
def nextStep():
    active = Step.query.filter_by(state='A').first()
    inactive = Step.query.filter_by(state='I').order_by(Step.order).first()

    if(active != None):
        active.state = 'D'
        active.end = datetime.utcnow()
        db.session.add(active)
        db.session.commit()

    if(inactive != None):
        inactive.state = 'A'
        inactive.start = datetime.utcnow()
        db.session.add(inactive)
        db.session.commit()

# Helper method to save a new message
def addMessage(message):
    l = Log()
    l.text = message
    l.time = datetime.utcnow()

    db.session.add(l)
    db.session.commit()
    # Update all connected clients
    socketio.emit('logupdate', l.to_json(), namespace ='/brew')

## REST Endpoints
@app.route("/data")
def data():

    return json.dumps({"steps":getAsArray(Step), 
        "temps": getAsArray(Temperatur), 
        "brew_name": Config.getParameter("brew_name", "No Name"),
        "heats": globalprops.heatLog,
        "gpios": getAllGPIO(),
        "pid": globalprops.pidState,
        "logs": getAsArray(Log)})

@app.route("/gpio")
def gpio():
    return json.dumps(getAllGPIO())

## Get all stored steps
@app.route("/steps")
def steps():
	return json.dumps(getAsArray(Step))

## Get all stored temps
@app.route("/temps")
def temps():
	return json.dumps(getAsArray(Temperatur))

@app.route("/heats")
def heats():
    return json.dumps(globalprops.heatLog)

## Get all logs
@app.route("/logs")
def logs():
	return json.dumps(getAsArray(Log))


## WebSocket Endpoints
@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT"

@socketio.on('start', namespace='/brew')
def ws_start():
    nextStep()
    socketio.emit('steps', getAsArray(Step), namespace ='/brew')
    addMessage("Start Brauprozess")

@socketio.on('next', namespace='/brew')
def ws_next():
    nextStep()
    socketio.emit('steps', getAsArray(Step), namespace ='/brew')
    

@socketio.on('reset', namespace='/brew')
def ws_reset():
    a = Step.query.all()
    
    for e in a:
        e.state = 'I'
        e.timer_start = None
        e.start = None
        e.end = None
        db.session.add(e)
        db.session.commit()

    socketio.emit('steps', getAsArray(Step), namespace ='/brew')
    addMessage("Brauprozess zuruecksetzen")

## Add custom log entry
@socketio.on('addlog', namespace='/brew')
def ws_addlog(message):
    addMessage(message)