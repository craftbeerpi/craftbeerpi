from flask import Blueprint, render_template, jsonify, request, url_for, current_app, redirect, request_started
from model import *
from step import nextStep, resetSteps, init
import json
from brewapp import app, socketio
from brewapp.base.util import *
from brewapp.base.brewrest import brewrestapi
import flask.ext.restless
import os
from blinker import Namespace
import time

my_signals = Namespace()
model_saved = my_signals.signal('model-saved')

@model_saved.connect_via(app)
def woohoo2(test, **extras):
    print "WWOOHOOO 2"


@model_saved.connect_via(app)
def woohoo3(test, **extras):

    for arg in extras:

        print "another arg:", extras[arg]
    print "WWOOHOOO 4"

steps = Blueprint('steps', __name__, template_folder='templates', static_folder='static' , static_url_path='/static')

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

#@request_started.connect_via(app)
#def woohoo(test, **extra):
#    print test
#    print request
#    print extra

def post_patch_many(**kw):
    init()

def post_get(result=None,**kw):
    result["objects"] = sorted(result["objects"], key=lambda k: k['order'])

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Step, methods=['GET', 'POST', 'DELETE', 'PUT'],allow_patch_many=True, postprocessors={'PATCH_SINGLE': [post_patch_many], 'DELETE_SINGLE': [post_patch_many], 'POST': [post_patch_many],'GET_MANY': [post_get]})


@brewjob(key="test")
def sendSign():
    while(True):
        print "SEND"
        model_saved.send(app, data="HALLO")
        time.sleep(3)

    s = Step()



@steps.route('/')
def index():
    return steps.send_static_file("index.html")


@steps.route('/steps')
def allSteps():
    return json.dumps(app.brewapp_steps)

@socketio.on('reset', namespace='/brew')
def ws_reset():
    resetSteps()

@socketio.on('start', namespace='/brew')
def ws_start():
    nextStep()
    addLogMessage("Start brewing process")

@socketio.on('next', namespace='/brew')
def ws_next_step():
    nextStep()
    addLogMessage("Next Step")
    pass
