from flask import Blueprint, render_template, jsonify, redirect, url_for
import json
from brewapp import app, socketio
from util import *
from model import *


base = Blueprint('base', __name__, template_folder='templates', static_folder='static')

@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "WS-CONNECT"

