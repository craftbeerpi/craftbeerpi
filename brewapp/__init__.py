from flask import Flask, abort, redirect, url_for, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from thread import start_new_thread
import logging
import flask_restless
from logging.handlers import RotatingFileHandler
import time
import os


import inspect

from functools import wraps


app = Flask(__name__)

logging.basicConfig(filename='./log/app.log',level=logging.DEBUG)

app.logger.info("##########################################")
app.logger.info("### NEW STARTUP Version 2.2")
from functools import wraps


app = Flask(__name__)
app.logger.info("##########################################")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../craftbeerpi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'craftbeerpi'
app.config['UPLOAD_FOLDER'] = './upload'


socketio = SocketIO(app)

## Custom Parameter
app.cbp = {}
app.brewapp_controller = {}
app.brewapp_automatic = {}
app.brewapp_automatic_state = {}
app.brewapp_fermenters = {}
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
app.brewapp_thermometer_cfg = {}
app.brewapp_thermometer_log = {}
app.brewapp_thermometer_last = {}


## Create Database
db = SQLAlchemy(app)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)


## Import modules (Flask Blueprints)
from .base.views import base
#from .module1.views import mymodule
from .ui.views import ui


if os.path.exists("craftbeerpi.db"):
    app.createdb = False
else:
    app.createdb = True

## Create Database
db.create_all()

## Register modules (Flask Blueprints)
app.register_blueprint(base,url_prefix='/base')
app.register_blueprint(ui,url_prefix='/ui')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/')
def index():
    return redirect('ui')

## Invoke Initializers
app.logger.info("## INITIALIZE DATA")
app.brewapp_init = sorted(app.brewapp_init, key=lambda k: k['order'])

for i in app.brewapp_init:
    if(i.get("config_parameter") != None):
        param = app.brewapp_config.get(i.get("config_parameter"), False)
        if(param == 'False'):
            continue
    app.logger.info("--> Method: " + i.get("function").__name__ + "() File: "+ inspect.getfile(i.get("function")))
    i.get("function")()

## Start Background Jobs
def job(key, interval, method):

    app.logger.info("Start Job: " + method.__name__ + " Interval:" + str(interval) + " Key:" + key)
    while app.brewapp_jobstate[key]:
        try:
            method()
        except Exception as e:
            print e
            app.logger.error("Exception" + method.__name__ + ": " + str(e))
        socketio.sleep(interval)



app.logger.info("## INITIALIZE JOBS")

for i in app.brewapp_jobs:


    if(i.get("config_parameter") != None):
        param = app.brewapp_config.get(i.get("config_parameter"), False)
        if(param == 'False'):
            continue
    app.brewapp_jobstate[i.get("key")] = True
    t = socketio.start_background_task(target=job, key=i.get("key"), interval=i.get("interval"), method=i.get("function"))

    app.logger.info("--> Method:" + i.get("function").__name__ + "() File: "+ inspect.getfile(i.get("function")))


