import os
from subprocess import Popen, PIPE, call
from random import randint, uniform
from brewapp import app

def getW1Thermometer():
    try:
        arr = []
        for dirname in os.listdir('/sys/bus/w1/devices'):
            if(dirname != "w1_bus_master1"):
                arr.append(dirname)
        return arr
    except:
        return ["DummySensor1","DummySensor2"]

def tempData1Wire(tempSensorId):
    try:
        ## Test Mode
        if(tempSensorId == None or tempSensorId == ""):
            return -1
        print "TEST MODE", app.testMode
        if (app.testMode == True):
            print "READ"
            pipe = Popen(["cat","w1_slave"], stdout=PIPE)
        else:
            pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)
        result = pipe.communicate()[0]
        ## parse the file
        if (result.split('\n')[0].split(' ')[11] == "YES"):
            temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
        else:
            temp_C = -99 #bad temp reading
    except Exception as e:
        #app.logger.warning(e)
        temp_C = round(randint(0,50),2)

    return round(temp_C,2)
