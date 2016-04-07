from flask import Blueprint, render_template, jsonify
import json
from brewapp import app, socketio

mymodule = Blueprint('mymodule', __name__, template_folder='templates', static_folder='static')

## Index Page for mymodule http://<server>:5000/mymodlue/
@mymodule.route('/')
def index():
    return mymodule.send_static_file("index.html")

## Web Socket Connection
@socketio.on('connect', namespace='/mymodule')
def ws_connect():
    print "CONNECT"
