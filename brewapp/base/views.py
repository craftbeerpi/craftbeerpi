from flask import Blueprint, render_template, jsonify
from model import *
import gpio
from gpio import setState, toggle
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

#@profile.route('/', defaults={'page': 'index'})

#@base.route('/<page>')
#def timeline(page):
    # Do some stuff
#    return render_template("index.html")

@base.route('/')
def index():
    # Do some stuff
    print app.testMode
    return render_template("index.html")

@base.route('/data')
def data():
    return json.dumps({"gpio":gpio.gpio_state,
        "steps":getAsArray(Step, Step.order),
        "chart":app.brewapp_chartdata})

@base.route("/steps")
def steps():
	return json.dumps(getAsArray(Step))

@base.route("/gpio/<gpio>/<state>")
def gpio_set_state(gpio, state):
    result = setState(gpio, state)
    #socketio.emit('gpio', json.dumps(), namespace ='/brew')
    return result

@base.route("/gpio/state")
def gpio_state():
    return json.dumps(gpio.gpio_state)

@base.route("/gpio/config")
def gpio_config():
	return json.dumps(getAsArray(GpioConfig))

@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT"

@socketio.on('gpio', namespace='/brew')
def ws_gpio(name):
    toggle(name)
    print "NAME: ", name
    socketio.emit('gpio_update', gpio.gpio_state, namespace ='/brew')
    #result = setState(name,"toggle")
