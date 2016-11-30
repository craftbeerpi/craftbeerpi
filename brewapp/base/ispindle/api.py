import os
import StringIO
import csv
import datetime
from brewapp import app, socketio, manager
from flask import make_response, send_from_directory, request
from brewapp.base.actor import *


def calc_wort(temp, angle):
    ### here the wort needs to be calculated
    pass

@app.route('/api/spindle/', methods=['POST'])
def receive_spindle_data():
    data = request.get_json()
    wort = calc_wort(data["temperature"], data["angle"])
    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()) * 1000
    writeSpindle("S_1", timestamp, data["temperature"], data["angle"], data["battery"])
    return ('', 204)