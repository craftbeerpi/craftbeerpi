from brewapp import app

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    print "IMPORT OK"
except:
    print "GPIO IMPRT ERROR", str(e)
    pass

class BrewGPIO(object):

    print "HLALLO"


    def init(self):
        try:
            for vid in app.brewapp_kettle_state:
                app.logger.info("## Kettle: " + str(vid))

                ## Init Heater
                heater_gpio = app.brewapp_kettle_state[vid]["heater"]["gpio"]
                if(heater_gpio != None and heater_gpio != ""):
                    app.logger.info("SETUP GPIO HEATER: " + str(app.brewapp_kettle_state[vid]["heater"]["gpio"]))
                    GPIO.setup(int(app.brewapp_kettle_state[vid]["heater"]["gpio"]), GPIO.OUT)
                    GPIO.output(app.brewapp_kettle_state[vid]["heater"]["gpio"], 1)

                ## Init Agiator
                agiator_gpio = app.brewapp_kettle_state[vid]["agitator"]["gpio"]
                print agiator_gpio
                if(agiator_gpio != None and agiator_gpio != ""):
                    app.logger.info("SETUP GPIO AGITATOR" + str(app.brewapp_kettle_state[vid]["agitator"]["gpio"]))
                    GPIO.setup(app.brewapp_kettle_state[vid]["agitator"]["gpio"], GPIO.OUT)
                    GPIO.output(app.brewapp_kettle_state[vid]["agitator"]["gpio"], 1)
            app.brewapp_gpio = True
            app.logger.info("ALL GPIO INITIALIZED")
            print "GPIO OK"
        except Exception as e:
            print "GPIO ERROR", str(e)
            app.logger.error("SETUP GPIO FAILD " + str(e))
            app.brewapp_gpio = False

    def getDevices(self):
        gpio = []
        for i in range(1, 40):
            gpio.append("GPIO"+str(i))
        return gpio

    def translateDeviceName(self, name):
        return name[4:]

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))
        if(app.brewapp_gpio == True):
            print self.translateDeviceName(device)
            GPIO.output(gpio, 0)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(device))

    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
        if(app.brewapp_gpio == True):
            print self.translateDeviceName(device)
            GPIO.output(gpio, 1)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))
