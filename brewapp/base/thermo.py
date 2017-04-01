import os
import StringIO
import csv
import datetime
from datetime import date

from flask import make_response, send_from_directory, request
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

@brewjob(key="readtemp", interval=5)
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



            if app.brewapp_config.get("UNIT", "C") == "F":
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


@app.route('/api/temp/<type>/<id>/chart')
def temp_chart(type, id):
    #return send_from_directory('../log', type + '_' + str(id) + '.templog'"", as_attachment=True, attachment_filename="Temp.log")

    id = int(id)


    name = "---"

    if type == "K":

        name = app.brewapp_kettle_state[id].get("name", "---")
    if type == "F":
        name = app.cbp['FERMENTERS'][id].get("name", "---")

    result = {"name": name, "data": read_temp_log('./log/' + type + '_' + str(id) + '.templog')}


    if type == 'F':
        hydrometer_id = app.cbp['FERMENTERS'][id].get("hydrometerid", None)

        if hydrometer_id is not None:

            hydrmeter_data = read_hydrometer_log('./log/S_' + str(hydrometer_id) + '.templog')

            if hydrmeter_data is not None:
                result["data"].update(hydrmeter_data)

    return json.dumps(result)




@app.route('/api/temp/<type>/<id>/chart', methods=["DELETE"])
def delete_temp_file(type, id):
    id = int(id)

    import os
    if type == "F":
        hydrometer_id = app.cbp['FERMENTERS'][id].get("hydrometerid", None)
        if hydrometer_id is not None:
            delete_file("./log/S_" + str(hydrometer_id) + ".templog")
    delete_file("./log/"+type + '_' + str(id) +".templog")

    return ('', 204)


