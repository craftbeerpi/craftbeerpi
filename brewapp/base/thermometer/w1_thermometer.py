import os
from subprocess import Popen, PIPE, call
from random import randint, uniform
from brewapp import app
from decimal import Decimal, ROUND_HALF_UP
from subprocess import call

class OneWireThermometer(object):

    def init(self):
        try:
            call(["modprobe", "w1-gpio"])
            call(["modprobe", "w1-therm"])
        except Exception as e:
            app.logger.error("Failed to initialize 1 wire thermometer ERROR: " + str(e))

    def getSensors(self):
        try:
            arr = []
            for dirname in os.listdir('/sys/bus/w1/devices'):
                if(dirname.startswith("28") or dirname.startswith("10")):
                    arr.append(dirname)
            return arr
        except:
            return ["1WDummySensor1","1W    DummySensor2"]

    def readTemp(self, tempSensorId):

        try:
            ## Test Mode
            if(tempSensorId == None or tempSensorId == ""):
                return None
            if (app.testMode == True):
                pipe = Popen(["cat","w1_slave"], stdout=PIPE)
            else:
                pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)
            result = pipe.communicate()[0]
            ## parse the file
            if (result.split('\n')[0].split(' ')[11] == "YES"):
                temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
            else:
                return None
        except Exception as e:
            app.logger.warning("Error" + str(e))

            return None

        return float(format(temp_C, '.2f'))
