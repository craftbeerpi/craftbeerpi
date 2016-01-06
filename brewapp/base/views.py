from flask import Blueprint, render_template, jsonify
import json
from brewapp import app, socketio
from util import *
from model import *

base = Blueprint('base', __name__, template_folder='templates', static_folder='static')


@base.route('/')
def index():
    return base.send_static_file("index.html")


@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT"
