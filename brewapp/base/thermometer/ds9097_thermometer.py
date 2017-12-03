import os
from subprocess import Popen, PIPE, call
import shlex
from random import randint, uniform
from brewapp import app
from decimal import Decimal, ROUND_HALF_UP
import os.path
from glob import glob

class DS9097Thermometer(object):

    def init(self):
        try:
            port = app.brewapp_config['THERM_DS9097_PORT']
            if not port or not os.path.exists(port):
                port = glob('/dev/ttyUSB*')[0]
                if not port:
                    app.logger.warn("Could not find %s or and /dev/ttyUSB*, exiting",
                                    app.brewapp_config['THERM_DS9097_PORT'])
                app.logger.warn("Could not find %s, using %s instead",
                                 app.brewapp_config['THERM_DS9097_PORT'], port)

            init_proc = Popen(shlex.split(
                'digitemp_DS9097 -q -s %s -i'%port
                ), stdout=PIPE, stderr=PIPE)
            ret = init_proc.wait()
            if ret != 0:
                app.logger.warning("Could not find sensors: \n'''\n%s\n%s\n'''\n",
                        init_proc.stdout.read(), init_proc.stderr.read())

        except Exception as e:
            app.logger.warning("Could not find sensors: %s", e)

    def readAllSensors(self):
        find_proc = Popen(shlex.split(
            'digitemp_DS9097 -q -o 2 -a'
            ), stdout=PIPE, stderr=PIPE)
        retVal = find_proc.wait()
        if retVal != 0:
            app.logger.warning("Could not enumerate sensors: \n'''\n%s\n%s\n'''\n",
                    find_proc.stdout.read(), find_proc.stderr.read())
            return {}

        ret = {}
        for line in find_proc.stdout.readlines():
            try:
                sid, temp = [x.strip().replace('\n', '') for x in line.split('\t', 1)]
                sid = "DS9097-%s"%sid
                temp = float(temp)
            except Exception as e:
                app.logger.warning("Could not enumerate sensors: %s", e)
                return {}
            ret[sid] = temp
        return ret


    def getSensors(self):
        try:
            sensors = self.readAllSensors()
            return list(sensors.keys())
        except:
            return []

    def readTemp(self, tempSensorId):
        try:
            ## Test Mode
            if(tempSensorId == None or tempSensorId == ""):
                return None
            sensors = self.readAllSensors()
            return sensors[tempSensorId]
        except Exception as e:
            app.logger.warning("Could not read temp sensor %s: %s", tempSensorId, e)
            return None
