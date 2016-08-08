from flask import Blueprint, render_template, jsonify, redirect, url_for
import json
from brewapp import app, socketio
from util import *
from model import *

base = Blueprint('base', __name__, template_folder='templates', static_folder='static')

setup_state = False

@base.route('/')
def index():
    print "HALLOOOOOO"
    if(Kettle.query.count() == 0):
        return redirect(url_for('base.setup'))
    else:
        print "HALLO"
        return redirect(url_for('base.index'))
        #return base.send_static_file("index.html")

@base.route('/index')
def index2():
    print "REDIRECT"
    return base.send_static_file("index.html")

@socketio.on('connect', namespace='/brew')
def ws_connect():
    print "CONNECT111"
