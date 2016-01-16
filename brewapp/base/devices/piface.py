from brewapp import app

try:
    import pifacedigitalio as piface
    app.logger.info("SETUP PiFace Module Loaded")
except:
    app.logger.error("SETUP PiFace Module " + str(e))
    pass

class PiFace(object):

    ## initialize the piface
    def init(self):
        piface.init()
        pass

    ## Returns the possible conntores as string
    def getDevices(self):
        gpio = []
        for i in range(1, 2):
            gpio.append("GPIO"+str(i))
        return gpio

    def translateDeviceName(self, name):
        if(name == None or name == ""):
            return None
        return int(name[4:])

    def switchON(self, device):
        gpio = self.translateDeviceName(device)
        piface.digital_write(gpio,1)
        pass

    def switchOFF(self, device):
        gpio = self.translateDeviceName(device)
        piface.digital_write(gpio,0)
        pass
