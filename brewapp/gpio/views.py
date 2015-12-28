from flask import Blueprint, render_template, jsonify
from model import *
import json
from brewapp import app, socketio
from brewapp.gpio.gpio import toggle

gpios = Blueprint('gpios', __name__, template_folder='templates', static_folder='static')

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

@gpios.route('/')
def index():
    # Do some stuff
    print app.testMode
    return render_template("index.html")

@gpios.route("/gpio/<gpio>/<state>")
def gpio_set_state(gpio, state):
    result = setState(gpio, state)
    #socketio.emit('gpio', json.dumps(), namespace ='/brew')
    return result

@gpios.route("/gpio/state")
def gpio_state():
    return json.dumps(gpio.gpio_state)

@gpios.route("/jobs")
def jobs():
    jobs = []
    for i in app.brewapp_jobs:
        jobs.append({"name": i.get("function").__name__})
    return json.dumps(jobs)

@gpios.route("/gpio/config")
def gpio_config():
	return json.dumps(getAsArray(GpioConfig))

@socketio.on('gpio', namespace='/brew')
def ws_gpio(name):
    print "NAME: ", name
    toggle(name)
    socketio.emit('gpio_update', app.brewapp_gpio_state, namespace ='/brew')
    #result = setState(name,"toggle")
