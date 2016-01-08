import os
from subprocess import Popen, PIPE, call
from random import randint, uniform

def getW1Thermometer():
    try:
        arr = []
        for dirname in os.listdir('/sys/bus/w1/devices'):
            if(dirname != "w1_bus_master1"):
                arr.append(dirname)
        return arr
    except:
        return ["ABC","CDE"]

def tempData1Wire(tempSensorId):
    print "SensorID" + tempSensorId
    try:
        ## Test Mode
        if (app.testMode == True):
            print "test mode"
            pipe = Popen(["cat","w1_slave"], stdout=PIPE)
        else:
            print "Read Temp"
            pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)
        result = pipe.communicate()[0]
        ## parse the file
        if (result.split('\n')[0].split(' ')[11] == "YES"):
            temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
        else:
            temp_C = -99 #bad temp reading
    except Exception as e:
        temp_C = round(randint(0,50),2)

    print temp_C
    return round(temp_C)
