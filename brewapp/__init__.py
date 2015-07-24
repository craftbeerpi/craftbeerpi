from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from subprocess import call
import json

app = Flask(__name__)
socketio = SocketIO(app)

try:
	call(["modprobe", "w1-gpio"])
	call(["modprobe", "w1-therm"])
except:
	print "ModeProbe Failed"




import brewapp.banner
import brewapp.model
import brewapp.globalprops




import brewapp.views
## Database models
## Agitator HTTP and WebSocket Endpoints
## Heating HTTP and WebSocket Endpoints
## PID HTTP and WebSocket Endpoints
import brewapp.pid
## Background Jobs
import brewapp.job
## Admin Console Config
import brewapp.admin
import brewapp.gpio
