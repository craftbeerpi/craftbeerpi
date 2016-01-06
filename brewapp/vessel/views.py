from flask import Blueprint, render_template, jsonify, request
from model import *
import json
from brewapp import app, socketio, db
from brewapp.base.util import *
import time
from random import randint, uniform
from pid import *
from gpio import *
from w1_thermometer import *


app.brewapp_vessel_automatic = {}
app.brewapp_vessel_temps = {}
app.brewapp_vessel_temps_log = {}

vessel = Blueprint('vessel2', __name__, template_folder='templates', static_folder='static')

@vessel.route('/')
def index():
    return render_template("vesselmain.html")

@vessel.route('/chart')
def chart():
    print "CHART"
    return render_template("chartmain.html")

@vessel.route('/data')
def vesselData():

    return json.dumps({"vessel": app.brewapp_vessel, "vessel_temps": app.brewapp_vessel_temps, "vessel_temp_log": app.brewapp_vessel_temps_log})

#@vessel.route('/vessel/<vid>')
#def vesseldata(vid):
#    return json.dumps(Vessel.query.get(vid).to_json());

@vessel.route('/chartdata/<vid>')
def chartdata(vid):
    return json.dumps(app.brewapp_vessel_temps_log[int(vid)])

@vessel.route('/get/thermometer')
def getTermometer():
    try:
        arr = []
        for dirname in os.listdir('/sys/bus/w1/devices'):
            if(dirname != "w1_bus_master1"):
                arr.append(dirname)

        return json.dumps(arr)
    except:
        return json.dumps(['ABC','CDE'])


@vessel.route('/templog')
def vesselTemplog():
    return json.dumps(app.brewapp_vessel_temps_log)

@vessel.route('/setup/<num>', methods=['POST'])
def vessel1Setup(num):

    number = int(num)
    if(request.method == 'POST'):
        if(number == 1 or number == 2 or number == 3):
            print "MASHTUN"
            mt = Vessel()
            mt.name = "MashTun"
            mt.sensorid = ""
            mt.target_temp = 0
            mt.height = 0
            mt.diameter = 0
            db.session.add(mt)

        if(number == 2 or number == 3):
            print "BOILTANK"
            bt = Vessel()
            bt.name = "Boil Tank"
            bt.sensorid = ""
            bt.target_temp = 0
            bt.height = 20
            bt.diameter = 20
            db.session.add(bt)

        if(number == 3):
            print "HOT Liquor"
            hlt = Vessel()
            hlt.name = "Hot Liquor Tank"
            hlt.sensorid = ""
            hlt.target_temp = 0
            hlt.height = 20
            hlt.diameter = 20
            db.session.add(hlt)
        db.session.commit();
        print "COMMIT ##########"
        initVessel()
        return json.dumps({})


@vessel.route('/<vid>', methods=['DELETE','GET','POST','PUT'])
def vesselupdate(vid):

    print "VID", vid
    print "METHOD", request.method
    if(request.method == 'DELETE'):
        print "DELETE VID", vid
        Vessel.query.filter_by(id=vid).delete()
        db.session.commit()
        initVessel()
        return json.dumps({})
    if(request.method == 'PUT'):
        print "SAVE VID", vid
        new_data = request.get_json()
        old_data = Vessel.query.get(new_data["id"])
        old_data.name = new_data["name"]
        old_data.sensorid = new_data["sensorid"]
        old_data.heater = new_data["heater"]["gpio"]
        old_data.agitator = new_data["agitator"]["gpio"]
        old_data.height = new_data["height"]
        old_data.diameter = new_data["diameter"]
        db.session.add(old_data);
        db.session.commit()
        initVessel(False)
    if(request.method == 'POST'):
        new_data = request.get_json()
        print new_data
        v = Vessel()
        v.name = new_data["name"]
        db.session.add(v);
        db.session.commit()
        initVessel()
    if(request.method == 'GET'):
        print "GET VID", vid

    return json.dumps(Vessel.query.get(vid).to_json());


@vessel.route('/templog/clear')
@socketio.on('/templog/clear', namespace='/brew')
def vesselTemplogClear():
    VesselTempLog.query.delete()
    db.session.commit()
    app.brewapp_vessel_temps_log = {}
    for vid in app.brewapp_vessel:
        app.brewapp_vessel_temps_log[vid] = []
    return ""


@socketio.on('vessel_automatic', namespace='/brew')
def ws_vessel_automatic(vesselid):
    print "Vessel", vesselid
    for vid in app.brewapp_vessel:
        if( vid == vesselid):
            if(app.brewapp_vessel[vid].get("automatic") == True):
                app.brewapp_vessel[vid]["automatic"] = False
                stopPID(vid)
            else:
                app.brewapp_vessel[vid]["automatic"] = True
                startPID(vid)
    socketio.emit('vessel_update', app.brewapp_vessel, namespace ='/brew')



@socketio.on('vessel_gpio', namespace='/brew')
def ws_gpio(gpio):
    for vid in app.brewapp_vessel:
        toogle(vid, "heater", gpio)
        toogle(vid, "agitator", gpio)
    socketio.emit('vessel_update', app.brewapp_vessel, namespace ='/brew')

def setTargetTemp(vid, temp):
    vessel = Vessel.query.get(vid)
    vessel.target_temp = temp
    db.session.add(vessel)
    db.session.commit()
    app.brewapp_vessel[vid]["target_temp"] = temp
    socketio.emit('vessel_update', app.brewapp_vessel, namespace ='/brew')

@brewinit()
def initVessel(clearlog = True):
    app.brewapp_vessel = getAsDict(Vessel, "id")
    if(clearlog):
        for vid in app.brewapp_vessel:
            app.brewapp_vessel_temps_log[vid] = []
    #app.brewapp_target_temp_method = setTargetTemp
    initGPIO()
    socketio.emit('vessel_update', app.brewapp_vessel, namespace ='/brew')

@brewjob("vesseltempjob", 2)
def readVesseltemp():
    update = {}
    for vid in app.brewapp_vessel:
        vl = VesselTempLog()
        vl.vesselid = app.brewapp_vessel[vid].get("id")
        vl.time = datetime.utcnow()
        vl.value = tempData1Wire(app.brewapp_vessel[vid].get("sensorid"))
        update[vl.vesselid] = vl.to_json()
        app.brewapp_vessel_temps_log[vid] += [vl.to_json()]
        app.brewapp_vessel_temps = update
        db.session.add(vl)
        db.session.commit()

    socketio.emit('vessel_temp_update', update, namespace ='/brew')
    time.sleep(5)
