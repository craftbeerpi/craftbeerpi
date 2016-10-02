import os
import StringIO
import csv
import datetime
from datetime import date
from flask import make_response, send_from_directory
from brewapp.base.actor import *

app.brewapp_thermometers = {}
app.brewapp_thermometers_log = {}
app.brewapp_thermometer_last = {}

# Get all available sensors
@app.route('/api/thermometer/sensors', methods=['GET'])
def getPhysicalSensors():
    return  json.dumps(app.brewapp_thermometer.getSensors())


# Get all available sensors
@app.route('/api/thermometer/sensors/active', methods=['GET'])
def getConfiguredSensors():
    return  json.dumps(app.brewapp_thermometers)


# GET all last temperatures
@app.route('/api/thermometer/last', methods=['GET'])
def getAllLastTempLog():
    return json.dumps(app.brewapp_thermometer_last)


# GET last temperatures for a sensors
@app.route('/api/thermometer/<id>/last', methods=['GET'])
def getLastTempLog(id):
    return json.dumps(app.brewapp_thermometer_last[id])

@brewjob(key="readtemp", interval=1)
def readTemp():
    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds())*1000
    temps = {}

    for t in app.brewapp_thermometer_cfg:

        tid = app.brewapp_thermometer_cfg[t]

        if tid["config"]["thermometer"]["id"] in app.brewapp_thermometer.getSensors():

            # Read Temp
            temp = app.brewapp_thermometer.readTemp(tid["config"]["thermometer"]["id"])

            if temp is None:
                return
            # UNIT
            if app.brewapp_config.get("UNIT", "C") is "F":
                temp = float(format(9.0/5.0 * temp + 32, '.2f'))
            # OFFSET
            if app.brewapp_thermometer_cfg[t]["config"]["thermometer"]["offset"] is not None:
                temp = float(format(temp + float(app.brewapp_thermometer_cfg[t]["config"]["thermometer"]["offset"]), '.2f'))
            else:
                temp = float(format(temp, '.2f'))
            # Init array if not present
            if app.brewapp_thermometers_log.get(t, None) is None:
                app.brewapp_thermometers_log[t] = []
            # save data
            app.brewapp_thermometers_log[t] += [[timestamp, temp ]]
            app.brewapp_thermometer_last[t] = temp

    socketio.emit('temp_udpdate', app.brewapp_thermometer_last, namespace ='/brew')

@app.route('/api/temp/<id>/download')
@nocache
def temp_donwload(id):
    return send_from_directory('../log', str(id) + '.templog'"", as_attachment=True, attachment_filename="Temp.log")


@app.route('/api/temp/<id>/chart')
def temp_chart(id):
    return read_temp_log('./log/' + id + '.templog')


@app.route('/api/temp/<id>/chart', methods=["DELETE"])
def delete_temp_file(id):
    import os
    os.remove(os.path.join("./log", id+".templog"))
    return ('', 204)