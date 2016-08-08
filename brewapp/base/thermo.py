import StringIO
import csv
import datetime
from datetime import date
from flask import make_response

from brewapp.base.hardwareswitch import *

app.brewapp_thermometers = {}
app.brewapp_thermometers_log = {}
app.brewapp_thermometer_last = {}


@app.route('/api/thermometer/<id>/export')
def exportTemp(id):

        id = int(app.brewapp_kettle_state[int(id)]["sensorid"])
        si = StringIO.StringIO()
        cw = csv.writer(si)

        r = []
        for d in app.brewapp_thermometers_log[id]:
            r.append([date.fromtimestamp((d[0]/ 1000)).strftime('%Y-%m-%d %H:%M:%S'),d[1]])

        cw.writerow(["Time", "Temperature"])
        cw.writerows(r)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=%s.csv" % (id)
        output.headers["Content-type"] = "text/csv"
        return output


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


## Get all thermometer logs
@app.route('/api/thermometer', methods=['GET'])
def getAllTempLog():
    return json.dumps(app.brewapp_thermometers_log)


## Get log for a sensor id
@app.route('/api/thermometer/<id>', methods=['GET'])
def getTempLog(id):
    return json.dumps(app.brewapp_thermometers_log[int(id)])

@app.route('/api/thermometer/target/temp/<id>', methods=['GET'])
def getTargetTempLog(id):
    return json.dumps(app.brewapp_kettle_target_temps_log[int(id)])


@app.route('/api/thermometer/kettle/<id>', methods=['GET'])
def getKettleTemp(id):
    sensorid =  app.brewapp_kettle_state[int(id)]["sensorid"]
    print sensorid
    return json.dumps({"target": app.brewapp_kettle_target_temps_log[int(id)], "temp": app.brewapp_thermometers_log[int(sensorid)]})

# Clear all temp logs
@app.route('/api/thermometer/clear', methods=['POST'])
def clearTemps():
    app.brewapp_thermometers_log = {}
    app.brewapp_kettle_target_temps_log = {}
    return ('',204)


#@brewinit()
def initThermo():
    thermometers = Hardware.query.filter_by(type='T').all()
    for t in thermometers:
        t2 = to_dict(t)
        t2['config'] = json.loads(t2['config'])
        app.brewapp_thermometers[t2['id']] = t2


@brewjob(key="readtemp2", interval=5)
def readTemp():


    timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds())*1000
    temps = {}

    for t in app.brewapp_thermometer_cfg:
        tid = app.brewapp_thermometer_cfg[t]
        if tid["config"]["thermometer"]["id"] in app.brewapp_thermometer.getSensors():

            # Read Temp
            temp = app.brewapp_thermometer.readTemp(tid["config"]["thermometer"]["id"])

            # UNIT
            if app.brewapp_config.get("UNIT", "C") is "F":
                temp = float(format(9.0/5.0 * temp + 32, '.2f'))
            # OFFSET
            if app.brewapp_thermometer_cfg[t]["config"]["thermometer"]["offset"] is not None:
                #print "OFFSET %s" %(app.brewapp_thermometers[t]["config"]["thermometer"]["offset"])
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

    for k in app.brewapp_kettle_state:
        if app.brewapp_kettle_target_temps_log.get(k, None) is None:
            app.brewapp_kettle_target_temps_log[k] = []
        app.brewapp_kettle_target_temps_log[k] += [[timestamp, app.brewapp_kettle_state[k]["target_temp"]]]
