from brewapp import app
from brewapp.base.devices.hardwarebase import HardwareBase
try:
    import pifacedigitalio as piface
    app.logger.info("SETUP PiFace Module Loaded")
except Exception as e:
    app.logger.error("SETUP PiFace Module " + str(e))
    pass

class PiFace(HardwareBase):

    ## initialize the piface
    def init(self):
        piface.init()
        pass

    def cleanup(self):
        pass


    ## Returns the possible conntores as string
    def getDevices(self):
        gpio = []
        for i in range(0, 8):
            gpio.append("PiFace"+str(i))
        return gpio

    def translateDeviceName(self, name):
        if(name == None or name == ""):
            return None
        pin = int(name[6:])
        return pin

    def switchON(self, device):
        gpio = self.translateDeviceName(device)
        piface.digital_write(gpio,1)
        pass

    def switchOFF(self, device):
        gpio = self.translateDeviceName(device)
        piface.digital_write(gpio,0)
        pass
