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


app.brewapp_kettle_automatic = {}
app.brewapp_kettle_temps = {}
app.brewapp_kettle_temps_log = {}

kettle = Blueprint('kettle2', __name__, template_folder='templates', static_folder='static')

@kettle.route('/')
def index():
    return render_template("kettlemain.html")

@kettle.route('/chart')
def chart():
    print "CHART"
    return render_template("chartmain.html")

@kettle.route('/data')
def kettleData():

    return json.dumps({"kettle": app.brewapp_kettle, "kettle_temps": app.brewapp_kettle_temps, "kettle_temp_log": app.brewapp_kettle_temps_log})

#@kettle.route('/kettle/<vid>')
#def kettledata(vid):
#    return json.dumps(Kettle.query.get(vid).to_json());

@kettle.route('/chartdata/<vid>')
def chartdata(vid):
    return json.dumps(app.brewapp_kettle_temps_log[int(vid)])

@kettle.route('/get/thermometer')
def getTermometer():
    try:
        arr = []
        for dirname in os.listdir('/sys/bus/w1/devices'):
            if(dirname != "w1_bus_master1"):
                arr.append(dirname)

        return json.dumps(arr)
    except:
        return json.dumps(['ABC','CDE'])


@kettle.route('/templog')
def kettleTemplog():
    return json.dumps(app.brewapp_kettle_temps_log)

@kettle.route('/setup/<num>', methods=['POST'])
def kettle1Setup(num):

    number = int(num)
    if(request.method == 'POST'):
        if(number == 1 or number == 2 or number == 3):
            print "MASHTUN"
            mt = Kettle()
            mt.name = "MashTun"
            mt.sensorid = ""
            mt.target_temp = 0
            mt.height = 0
            mt.diameter = 0
            db.session.add(mt)

        if(number == 2 or number == 3):
            print "BOILTANK"
            bt = Kettle()
            bt.name = "Boil Tank"
            bt.sensorid = ""
            bt.target_temp = 0
            bt.height = 20
            bt.diameter = 20
            db.session.add(bt)

        if(number == 3):
            print "HOT Liquor"
            hlt = Kettle()
            hlt.name = "Hot Liquor Tank"
            hlt.sensorid = ""
            hlt.target_temp = 0
            hlt.height = 20
            hlt.diameter = 20
            db.session.add(hlt)
        db.session.commit();
        print "COMMIT ##########"
        initKettle()
        return json.dumps({})


@kettle.route('/<vid>', methods=['DELETE','GET','POST','PUT'])
def kettleupdate(vid):

    print "VID", vid
    print "METHOD", request.method
    if(request.method == 'DELETE'):
        print "DELETE VID", vid
        Kettle.query.filter_by(id=vid).delete()
        db.session.commit()
        initKettle()
        return json.dumps({})
    if(request.method == 'PUT'):
        print "SAVE VID", vid
        new_data = request.get_json()
        old_data = Kettle.query.get(new_data["id"])
        old_data.name = new_data["name"]
        old_data.sensorid = new_data["sensorid"]
        old_data.heater = new_data["heater"]["gpio"]
        old_data.agitator = new_data["agitator"]["gpio"]
        old_data.height = new_data["height"]
        old_data.diameter = new_data["diameter"]
        db.session.add(old_data);
        db.session.commit()
        initKettle(False)
    if(request.method == 'POST'):
        new_data = request.get_json()
        print new_data
        v = Kettle()
        v.name = new_data["name"]
        db.session.add(v);
        db.session.commit()
        initKettle()
    if(request.method == 'GET'):
        print "GET VID", vid

    return json.dumps(Kettle.query.get(vid).to_json());


@kettle.route('/templog/clear')
@socketio.on('/templog/clear', namespace='/brew')
def kettleTemplogClear():
    KettleTempLog.query.delete()
    db.session.commit()
    app.brewapp_kettle_temps_log = {}
    for vid in app.brewapp_kettle:
        app.brewapp_kettle_temps_log[vid] = []
    return ""


@socketio.on('kettle_automatic', namespace='/brew')
def ws_kettle_automatic(kettleid):
    print "Kettle", kettleid
    for vid in app.brewapp_kettle:
        if( vid == kettleid):
            if(app.brewapp_kettle[vid].get("automatic") == True):
                app.brewapp_kettle[vid]["automatic"] = False
                stopPID(vid)
            else:
                app.brewapp_kettle[vid]["automatic"] = True
                startPID(vid)
    socketio.emit('kettle_update', app.brewapp_kettle, namespace ='/brew')



@socketio.on('kettle_gpio', namespace='/brew')
def ws_gpio(gpio):
    for vid in app.brewapp_kettle:
        toogle(vid, "heater", gpio)
        toogle(vid, "agitator", gpio)
    socketio.emit('kettle_update', app.brewapp_kettle, namespace ='/brew')

def setTargetTemp(vid, temp):
    kettle = Kettle.query.get(vid)
    kettle.target_temp = temp
    db.session.add(kettle)
    db.session.commit()
    app.brewapp_kettle[vid]["target_temp"] = temp
    socketio.emit('kettle_update', app.brewapp_kettle, namespace ='/brew')

@brewinit()
def initKettle(clearlog = True):
    app.brewapp_kettle = getAsDict(Kettle, "id")
    if(clearlog):
        for vid in app.brewapp_kettle:
            app.brewapp_kettle_temps_log[vid] = []
    #app.brewapp_target_temp_method = setTargetTemp
    initGPIO()
    socketio.emit('kettle_update', app.brewapp_kettle, namespace ='/brew')

@brewjob("kettletempjob", 2)
def readKettletemp():
    update = {}
    for vid in app.brewapp_kettle:
        vl = KettleTempLog()
        vl.kettleid = app.brewapp_kettle[vid].get("id")
        vl.time = datetime.utcnow()
        vl.value = tempData1Wire(app.brewapp_kettle[vid].get("sensorid"))
        update[vl.kettleid] = vl.to_json()
        app.brewapp_kettle_temps_log[vid] += [vl.to_json()]
        app.brewapp_kettle_temps = update
        db.session.add(vl)
        db.session.commit()

    socketio.emit('kettle_temp_update', update, namespace ='/brew')
    time.sleep(5)
