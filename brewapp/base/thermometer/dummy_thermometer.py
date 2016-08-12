import os, re
from subprocess import Popen, PIPE, call
from random import randint, uniform
from brewapp import app
from decimal import Decimal, ROUND_HALF_UP
from subprocess import call

class DummyThermometer(object):

    def init(self):
        pass

    def getSensors(self):
        return ["DummySensor1","DummySensor2"]

    def readTemp(self, tempSensorId):

        value = -1
        path = "test/w1_slave"

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

