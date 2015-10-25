from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from subprocess import call, Popen, PIPE
import json
import shlex

app = Flask(__name__)
socketio = SocketIO(app)

import brewapp.globalprops

if globalprops.owfsWin != True:
        try:
             call(["modprobe", "w1-gpio"])
       	     call(["modprobe", "w1-therm"])
        except:
             print "ModeProbe Failed"
else:        	
     try:
          cmd ='C:/Programme/OWFS/bin/owserver.exe -u -p 3000 --timeout_volatile=2'
          args = shlex.split(cmd)
          spipe = Popen(args, stdout = False)
     except:
          print "OWS Failed"
   

import brewapp.banner
import brewapp.model

import brewapp.gpio
import brewapp.job
import brewapp.views
## Database models
## Agitator HTTP and WebSocket Endpoints
## Heating HTTP and WebSocket Endpoints
## PID HTTP and WebSocket Endpoints
import brewapp.pid
## Background Jobs

## Admin Console Config
import brewapp.admin
