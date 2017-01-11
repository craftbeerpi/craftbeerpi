import os
from brewapp import app
from brewapp.base.actor import ActorBase
from brewapp.base.model import *

GPIO_PATH = '/sys/class/gpio'
GPIO_MAX  = 200
GPIO_MIN  = 0
GPIO_HIGH = '1'
GPIO_LOW  = '0'
GPIO_IN   = 'in'
GPIO_OUT  = 'out'

class GPIOSys(ActorBase):

    def setup(self, device, value):
        #echo <GPIO#>  > /sys/class/gpio/export
        #echo "in/out" > /sys/class/gpio/gpio<#>/direction
        if not os.path.exists(GPIO_PATH + ('/gpio%d' % device)):
            with open(GPIO_PATH + '/export', 'w') as fp:
                fp.write(str(device))
        with open( GPIO_PATH + ('/gpio%d/direction' % device), 'w') as fp:
            fp.write(value)

    def output(self, device, value):
        #echo "1/0" > /sys/class//gpiogpio<#>/value
        with open(GPIO_PATH + ('/gpio%d/value' % device), 'w') as fp:
            fp.write(value)

    def init(self):
        app.logger.info("INIT GPIO")
        try:
            app.logger.info(app.brewapp_hardware_config)
            for h in app.brewapp_hardware_config:

                hw = app.brewapp_hardware_config[h];
                app.logger.info(hw)

                g = self.translateDeviceName(hw["config"]["switch"])
                app.logger.info(g)

                if(g != None):
                    app.logger.info("SETUP HARDWARE: " + str(h) + " GPIO: " + str(g))
                    self.setup(g, GPIO_OUT)

                    if(self.getConfigValue(h, "inverted", False)):
                        app.logger.warning("SETUP INVERTED")
                        self.output(g, GPIO_HIGH)
                    else:
                        app.logger.warning("SETUP NOT INVERTED")
                        self.output(g, GPIO_LOW)

            app.brewapp_gpio = True
            self.state = True
            app.logger.info("ALL GPIO INITIALIZED")

        except Exception as e:
            app.logger.error("SETUP GPIO FAILED " + str(e))
            app.brewapp_gpio = False
            self.state = False

    def cleanup(self):
        # Turn off switches?
        # try:
        #     GPIO.cleanup()
        # except Exception as e:
        #     app.logger.error("CLEAN UP OF GPIO FAILED " + str(e))
        pass

    def getDevices(self):
        gpio = []
        for i in range(GPIO_MIN, GPIO_MAX):
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
                self.output(gpio, GPIO_LOW)
            else:
                app.logger.warning("SWITCH ON - Not Inverted")
                self.output(gpio, GPIO_HIGH)
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
                self.output(gpio, GPIO_HIGH)
            else:
                app.logger.warning("SWITCH OFF - Not Inverted")
                self.output(gpio, GPIO_LOW)
            pass
        else:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))

