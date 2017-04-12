from brewapp import app
from brewapp.base.actor import ActorBase
try:
    import pifacedigitalio as piface
    app.logger.info("SETUP PiFace Module Loaded")
except Exception as e:
    app.logger.error("SETUP PiFace Module " + str(e))
    pass

class PiFace(ActorBase):

    ## initialize the piface
    def init(self):
        app.logger.info("INIT PIFACE")
        try:
            piface.init()
            self.state = True
        except Exception as e:
            app.logger.error("SETUP PIFACE FAILED " + str(e))
            self.state = False

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
