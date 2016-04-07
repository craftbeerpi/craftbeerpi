from flask import Flask, abort, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask.ext.socketio import SocketIO, emit
from thread import start_new_thread
from flask_admin import AdminIndexView, expose
import logging
import flask.ext.restless
from logging.handlers import RotatingFileHandler
import time

import inspect


app = Flask(__name__)
socketio = SocketIO(app)

logging.basicConfig(filename='app.log',level=logging.DEBUG)

app.logger.info("##########################################")
app.logger.info("### NEW STARTUP")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SECRET_KEY'] = 'craftbeerpi'
app.config['UPLOAD_FOLDER'] = './upload'


app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_stepaction = []
app.brewapp_gpio = False
app.testMode = False
app.brewapp_jobstate = {}
app.brewapp_current_step = None
app.brewapp_button = {"next": 23, "reset": 24}
app.brewapp_kettle_state = {}
app.brewapp_pump_state = {}
app.brewapp_kettle = {}
app.brewapp_kettle_temps_log = {}
app.brewapp_kettle_automatic = {}
app.brewapp_pid_state =  {}
app.brewapp_pid = []
app.brewapp_switch_state = {}
app.brewapp_config = {}


## Create Database
db = SQLAlchemy(app)
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
## Import modules (Flask Blueprints)
from .base.views import base


## Create Database
db.create_all()

## Register modules (Flask Blueprints)
app.register_blueprint(base,url_prefix='/base')


@app.route('/')
def index():
    return redirect('base')

@app.route('/restart')
def restart():
    app.logger.info("--> RESTART TRIGGERED")
    start_new_thread(doRestart,())
    return redirect('base')

def doRestart():
    time.sleep(5)
    from subprocess import call
    app.logger.info("--> RESTART EXECUTE")
    call(["/etc/init.d/craftbeerpiboot", "restart"])


app.logger.info("## INITIALIZE DATA")
for i in app.brewapp_init:
    app.logger.info("--> Method: " + i.__name__ + "() File: "+ inspect.getfile(i))
    i()

from base.config import *
initDriver()
app.brewapp_hardware.init()
app.brewapp_thermometer.init()

def job(key, interval, method):
    while app.brewapp_jobstate[key]:
        method()
        time.sleep(interval)

app.logger.info("## INITIALIZE JOBS")
for i in app.brewapp_jobs:
    app.brewapp_jobstate[i.get("key")] = True
    start_new_thread(job,(i.get("key"),i.get("interval"),i.get("function")))
    app.logger.info("--> Method:" + i.get("function").__name__ + "() File: "+ inspect.getfile(i.get("function")))
