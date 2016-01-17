from brewapp import app

class HardwareBase(object):

    def init(self):
        pass

    def cleanup(self):
        pass

    def getDevices(self):
        gpio = []
        for i in range(1, 6):
            gpio.append("GPIO"+str(i))
        return gpio

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))


    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
