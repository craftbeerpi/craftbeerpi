from subprocess import Popen, PIPE, call
from brewapp import app, db, socketio
from brewapp.thermometer.model import *
from thread import start_new_thread
import time
from brewapp import brewjob, brewinit

## Method to read the temperatur
def tempData1Wire(tempSensorId):
    try:
        ## Test Mode
        if (app.testMode == True):
            pipe = Popen(["cat","w1_slave"], stdout=PIPE)
            ## GPIO Mod
        else:
            pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)
        result = pipe.communicate()[0]
        ## parse the file
        if (result.split('\n')[0].split(' ')[11] == "YES"):
            temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
        else:
            temp_C = -99 #bad temp reading
    except:
        temp_C = -1

    return temp_C

@brewjob(key="tempjob")
def readTemp():
    app.brewapp_chartdata["temp1"] = []
    while app.brewapp_jobstate["tempjob"]:
        app.brewapp_temperature["value1"] = tempData1Wire("ABC")
        t = Temperature()
        t.time = datetime.utcnow()
        t.value1 = app.brewapp_temperature["value1"]
        app.brewapp_chartdata["temp1"] += [[t.to_unixTime(), t.value1]]
        db.session.add(t)
        db.session.commit()
        update = [t.to_unixTime(), t.value1]
        
        socketio.emit('chart_update', update, namespace ='/brew')
        time.sleep( 5 )
    print "TEMP JOB STOPPED"

def clearData():
    Temperature.query.delete()
    db.session.commit()
    app.brewapp_chartdata = {}
    app.brewapp_chartdata["temp1"] = []


def loadThermometer():
    thermometer = db.session.query(ThermometerConfig).all()
    app.brewapp_thermometer = {}
    for t in thermometer:
        print t.name
        app.brewapp_thermometer[t.name] = -1

@brewinit()
def loadData():

    loadThermometer()
    temps = db.session.query(Temperature).all()
    x = 'temp1'
    app.brewapp_chartdata[x] = []
    for t in temps:
        x = 'temp1'
        app.brewapp_chartdata[x] += [[t.to_unixTime(), t.value1]]
