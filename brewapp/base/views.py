from flask import Blueprint, render_template, jsonify
import json
from brewapp import app, socketio
from util import *

base = Blueprint('base', __name__, template_folder='templates', static_folder='static')


@base.route('/')
def index():
    # Do some stuff
    return render_template("index.html")

@base.route('/data')
def data():
    return json.dumps({"gpio":app.brewapp_gpio_state,
        "steps":app.brewapp_steps,
        "log":app.brewapp_log,
        "thermometer": app.brewapp_thermometer,
        "chart":app.brewapp_chartdata})

@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT"
