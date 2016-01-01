from flask import Blueprint, render_template, jsonify
from model import *
import json
from brewapp import app, socketio
from log import *
from brewapp import app, db, socketio
from brewapp.base.util import *

log = Blueprint('log', __name__, template_folder='templates', static_folder='static')

def addMessage(message):
    l = Log()
    l.text = message
    l.time = datetime.utcnow()

    app.brewapp_log.append(l.to_json())
    db.session.add(l)
    db.session.commit()
    # Update all connected clients
    socketio.emit('logupdate', l.to_json(), namespace ='/brew')

@brewinit()
def loadLog():
    app.brewapp_log = getAsArray(Log)
    app.brewapp_log_method = addMessage

@log.route('/')
def index():
    return render_template("index.html")

@socketio.on('addlog', namespace='/brew')
def ws_addlog(message):
    addMessage(message)
