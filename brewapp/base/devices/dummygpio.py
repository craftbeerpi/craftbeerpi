from brewapp import app
from brewapp.base.hardwareswitch import SwitchBase
from brewapp.base.model import *

class DummyGPIO(SwitchBase):

    def init(self):
        print "INIT SWITCH"
        print app.brewapp_switch_state
        hw = Hardware.query.all()
        for h in hw:
            print h.switch

        hw = Kettle.query.all()
        for h in hw:
            print h.heater
            print h.agitator

    def cleanup(self):
        print "CLEAN UP"

    def getDevices(self):
        gpio = []
        for i in range(1, 6):
            gpio.append("GPIO"+str(i))
        return gpio

    def translateDeviceName(self, name):
        if(name == None or name == ""):
            return None
        return int(name[4:])

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))


    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
