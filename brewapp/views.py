from brewapp import app, socketio
from flask import render_template
from flask.ext.socketio import SocketIO, emit
import json
from brewapp.model import db, Step, Temperatur, Log, Config, getAsArray
import globalprops
from datetime import datetime, timedelta
from brewapp.gpio import gpio_state, getAllGPIO


## Index View
@app.route('/')
def index():
    return render_template("index.html" )

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
    #app.logger.debug('A value for debugging')
    return json.dumps({"steps":getAsArray(Step),
        "chart": globalprops.chart_cache,
        "temps": globalprops.temps,
        "brew_name": Config.getParameter("brew_name", "No Name"),
        "gpios": getAllGPIO(),
        "pid": globalprops.autoState,
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
    return json.dumps(globalprops.chart_cache)

@app.route("/temps/count")
def tempscount():
    return json.dumps(len(globalprops.chart_cache['temp1']))

@app.route("/heats")
def heats():
    return json.dumps(globalprops.heatLog)

## Get all logs
@app.route("/logs")
def logs():
	return json.dumps(getAsArray(Log))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

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
    db.session.query(Step).update({'state': 'I', 'start': None, 'end': None, 'timer_start': None},  synchronize_session='evaluate')
    db.session.commit()
    socketio.emit('steps', getAsArray(Step), namespace ='/brew')
    addMessage("Brauprozess zuruecksetzen")

## Add custom log entry
@socketio.on('addlog', namespace='/brew')
def ws_addlog(message):
    addMessage(message)
