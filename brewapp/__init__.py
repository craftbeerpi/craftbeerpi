from flask import Flask, abort, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO, emit
from thread import start_new_thread
import logging
import flask.ext.restless
from logging.handlers import RotatingFileHandler
import time
import os
import inspect


app = Flask(__name__)
socketio = SocketIO(app)

logging.basicConfig(filename='app.log',level=logging.DEBUG)

app.logger.info("##########################################")
app.logger.info("### NEW STARTUP")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
app.config['UPLOAD_FOLDER'] = './upload'

## Custom Parameter
app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_stepaction = []
app.brewapp_gpio = False
app.testMode = False
app.brewapp_jobstate = {}
app.brewapp_current_step = None
app.brewapp_kettle_state = {}
app.brewapp_pump_state = {}
app.brewapp_kettle = {}
app.brewapp_kettle_temps_log = {}
app.brewapp_kettle_target_temps_log = {}
app.brewapp_kettle_automatic = {}
app.brewapp_pid_state =  {}
app.brewapp_pid = []
app.brewapp_switch_state = {}
app.brewapp_hardware_config = {}
app.brewapp_config = {}


## Create Database
db = SQLAlchemy(app)
from flask_restless_swagger import SwagAPIManager as APIManager
manager = APIManager(app, flask_sqlalchemy_db=db)
#manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
## Import modules (Flask Blueprints)
from .base.views import base
from .module1.views import mymodule

if os.path.exists("craftbeerpi.db"):
    app.createdb = False
else:
    app.createdb = True

## Create Database
db.create_all()

## Register modules (Flask Blueprints)
app.register_blueprint(base,url_prefix='/base')
app.register_blueprint(mymodule,url_prefix='/mymodule')

@app.route('/')
def index():
    return redirect('base')

## Invoke Initializers
app.logger.info("## INITIALIZE DATA")
app.brewapp_init = sorted(app.brewapp_init, key=lambda k: k['order'])
for i in app.brewapp_init:

    app.logger.info("--> Method: " + i.get("function").__name__ + "() File: "+ inspect.getfile(i.get("function")))
    i.get("function")()

## Start Background Jobs
def job(key, interval, method):
    while app.brewapp_jobstate[key]:
        method()
        time.sleep(interval)

app.logger.info("## INITIALIZE JOBS")
for i in app.brewapp_jobs:
    app.brewapp_jobstate[i.get("key")] = True
    start_new_thread(job,(i.get("key"),i.get("interval"),i.get("function")))
    app.logger.info("--> Method:" + i.get("function").__name__ + "() File: "+ inspect.getfile(i.get("function")))
