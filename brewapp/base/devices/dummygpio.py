from brewapp import app

class DummyGPIO(object):

    def init(self):
        pass

    def getDevices(self):
        gpio = []
        for i in range(1, 40):
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
