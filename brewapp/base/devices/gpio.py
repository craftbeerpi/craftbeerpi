from brewapp import app
from brewapp.hardwarebase import HardwareBase

try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass

class BrewGPIO(HardwareBase):

    def init(self):
        try:
            GPIO.setmode(GPIO.BCM)
            for vid in app.brewapp_kettle_state:
                app.logger.info("## Kettle: " + str(vid))

                ## Init Heater
                heater_gpio = self.translateDeviceName(app.brewapp_kettle_state[vid]["heater"]["gpio"])
                if(heater_gpio != None and heater_gpio != ""):
                    app.logger.info("SETUP GPIO HEATER: " + str(app.brewapp_kettle_state[vid]["heater"]["gpio"]))
                    GPIO.setup(heater_gpio, GPIO.OUT)
                    GPIO.output(heater_gpio, 0)

                ## Init Agiator
                agiator_gpio = self.translateDeviceName(app.brewapp_kettle_state[vid]["agitator"]["gpio"])
                print agiator_gpio
                if(agiator_gpio != None and agiator_gpio != ""):
                    app.logger.info("SETUP GPIO AGITATOR" + str(app.brewapp_kettle_state[vid]["agitator"]["gpio"]))
                    GPIO.setup(agiator_gpio, GPIO.OUT)
                    GPIO.output(agiator_gpio, 0)
            app.brewapp_gpio = True
            app.logger.info("ALL GPIO INITIALIZED")
        except Exception as e:
            app.logger.error("SETUP GPIO FAILD " + str(e))
            app.brewapp_gpio = False

    def cleanup(self):
        print "CLEAN UP"
        GPIO.cleanup()

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
        if(app.brewapp_gpio == True):
            gpio = self.translateDeviceName(device)
            GPIO.output(gpio, 1)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(device))

    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
        if(app.brewapp_gpio == True):
            gpio = self.translateDeviceName(device)
            GPIO.output(gpio, 0)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))
