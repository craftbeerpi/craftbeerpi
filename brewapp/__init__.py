from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import globalprops

app = Flask(__name__)
socketio = SocketIO(app)

if globalprops.testMode == False:
        call(["modprobe", "w1-gpio"])
        call(["modprobe", "w1-therm"])

import brewapp.banner

import brewapp.views
## Agitator HTTP and WebSocket Endpoints
import brewapp.agitator
## Heating HTTP and WebSocket Endpoints
import brewapp.heating
## PID HTTP and WebSocket Endpoints
import brewapp.pid
## Background Jobs
import brewapp.job
## Database models
import brewapp.model
## Admin Console Config
import brewapp.admin

