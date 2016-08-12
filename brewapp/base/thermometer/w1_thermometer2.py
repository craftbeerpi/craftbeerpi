import os, re
from subprocess import Popen, PIPE, call
from random import randint, uniform
from brewapp import app
from decimal import Decimal, ROUND_HALF_UP
from subprocess import call


class OneWireThermometer2(object):

    def init(self):
        try:
            call(["modprobe", "w1-gpio"])
            call(["modprobe", "w1-therm"])
        except Exception as e:
            app.logger.error("Faild to initialize 1 wire thermometert ERROR: " + str(e))

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

        value = -1
        path = "/sys/bus/w1/devices/w1_bus_master1/"+tempSensorId+"/w1_slave"

        try:
            f = open(path, "r")
            line = f.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                line = f.readline()
                m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
                if m:
                    value = float(m.group(2)) / 1000.0
            f.close()
        except (Exception), e:
            app.logger.warning("Read temp failed " + str(e))

        return value

