from flask import Blueprint, render_template, jsonify
from model import *
from step import nextStep, resetSteps
import json
from brewapp import app, socketio

steps = Blueprint('steps', __name__, template_folder='templates', static_folder='static')


@steps.route('/')
def index():
    return render_template("index.html")

@steps.route('/steps')
def allSteps():
	return json.dumps(app.brewapp_steps)

@socketio.on('reset', namespace='/brew')
def ws_reset():
    resetSteps()

@socketio.on('start', namespace='/brew')
def ws_start():
    nextStep()


@socketio.on('next', namespace='/brew')
def ws_next_step():
    nextStep()
