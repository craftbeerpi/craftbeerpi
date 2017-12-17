from brewapp import app
from brewapp.base.actor import ActorBase
from brewapp.base.model import *
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
            app.brewapp_gpio=True
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
        app.logger.info("Output ON" + str(device))
        if(app.brewapp_gpio == True):

            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            gpio = self.translateDeviceName(switch_name)

            if self.getConfigValue(device, "inverted", False) :
                app.logger.warning("SWITCH ON - Inverted")
                piface.digital_write(gpio, 0)
            else:
                app.logger.warning("SWITCH ON - Not Inverted")
                piface.digital_write(gpio, 1)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(device))

    
    def switchOFF(self, device):
        app.logger.info("Output OFF" + str(device))
        if(app.brewapp_gpio == True):

            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            gpio = self.translateDeviceName(switch_name)

            if(self.getConfigValue(device, "inverted", False)):
                app.logger.warning("SWITCH OFF - Inverted")
                piface.digital_write(gpio, 1)
            else:
                app.logger.warning("SWITCH OFF - Not Inverted")
                piface.digital_write(gpio, 0)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))
