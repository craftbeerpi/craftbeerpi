from flask import Blueprint, render_template, jsonify
from model import *
import json
from brewapp import app, socketio

thermometer = Blueprint('thermometer', __name__, template_folder='templates', static_folder='static')

@thermometer.route('/')
def index():
    # Do some stuff
    print app.testMode
    return render_template("index.html")
