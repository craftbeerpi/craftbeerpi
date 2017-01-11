from brewapp import app
from brewapp.base.actor import ActorBase
from brewapp.base.model import *

try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass

class BrewGPIO(ActorBase):

    def init(self):
        app.logger.info("INIT GPIO")
        try:
            GPIO.setmode(GPIO.BCM)
            app.logger.info(app.brewapp_hardware_config)
            for h in app.brewapp_hardware_config:


                hw = app.brewapp_hardware_config[h];
                app.logger.info(hw)

                g = self.translateDeviceName(hw["config"]["switch"])
                app.logger.info(g)

                if(g != None):
                    app.logger.info("SETUP HARDWARE: " + str(h) + " GPIO: " + str(g))
                    GPIO.setup(g, GPIO.OUT)

                    if(self.getConfigValue(h, "inverted", False)):
                        app.logger.warning("SETUP INVERTED")
                        GPIO.output(g, 1)
                    else:
                        app.logger.warning("SETUP NOT INVERTED")
                        GPIO.output(g, 0)

            app.brewapp_gpio = True
            self.state = True
            app.logger.info("ALL GPIO INITIALIZED")

        except Exception as e:
            app.logger.error("SETUP GPIO FAILED " + str(e))
            app.brewapp_gpio = False
            self.state = False

    def cleanup(self):
        try:
            GPIO.cleanup()
        except Exception as e:
            app.logger.error("CLEAN UP OF GPIO FAILED " + str(e))

    def getDevices(self):
        gpio = []
        for i in range(2, 28):
            gpio.append("GPIO"+str(i))
        return gpio

    def translateDeviceName(self, name):
        if(name == None or name == ""):
            return None
        return int(name[4:])

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))
        if(app.brewapp_gpio == True):

            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            gpio = self.translateDeviceName(switch_name)

            if self.getConfigValue(device, "inverted", False) :
                app.logger.warning("SWITCH ON - Inverted")
                GPIO.output(gpio, 0)
            else:
                app.logger.warning("SWITCH ON - Not Inverted")
                GPIO.output(gpio, 1)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(device))

    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
        if(app.brewapp_gpio == True):

            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            gpio = self.translateDeviceName(switch_name)

            if(self.getConfigValue(device, "inverted", False)):
                app.logger.warning("SWITCH OFF - Inverted")
                GPIO.output(gpio, 1)
            else:
                app.logger.warning("SWITCH OFF - Not Inverted")
                GPIO.output(gpio, 0)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))
