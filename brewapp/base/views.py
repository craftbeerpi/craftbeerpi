from flask import Blueprint, render_template, jsonify
import json
from brewapp import app, socketio

base = Blueprint('base', __name__, template_folder='templates', static_folder='static')

def getAsArray(obj, order = None):

    print dir(order)
    if(order is not None):
        result =obj.query.order_by(order).all()
    else:
        result =obj.query.all()
    ar = []
    for t in result:
        ar.append(t.to_json())
    return ar

@base.route('/')
def index():
    # Do some stuff
    print app.testMode
    return render_template("index.html")

@base.route('/data')
def data():
    return json.dumps({"gpio":app.brewapp_gpio_state,
        "steps":app.brewapp_steps,
        "thermometer": app.brewapp_thermometer,
        "chart":app.brewapp_chartdata})

@base.route('/stop')
def stop():
    app.brewapp_jobstate["tempjob"] = False
    return "OK"

@base.route('/start')
def start():
    starttempJob()
    return "OK"


@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT"
