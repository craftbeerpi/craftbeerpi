try:
    import pifacedigitalio as piface
    app.logger.info("SETUP PiFace Module Loaded")
except:
    app.logger.error("SETUP PiFace Module " + str(e))
    pass

class PiFace(object):

    def init(self):
        piface.init()
        pass

    def getDevices(self):
        gpio = []
        for i in range(2, 6):
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
