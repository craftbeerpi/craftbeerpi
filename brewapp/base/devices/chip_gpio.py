from brewapp import app
from brewapp.base.actor import ActorBase

try:
    from CHIP_IO import GPIO
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))


class BrewGPIO(ActorBase):

    def init(self):
        app.logger.info("INIT GPIO")
        try:
            app.logger.info(app.brewapp_hardware_config)
            for h, hw in app.brewapp_hardware_config.items():
                app.logger.info(hw)

                g = hw["config"]["switch"]
                app.logger.info(g)

                if not g:
                    continue

                app.logger.info("SETUP HARDWARE: " + str(h) + " GPIO: " + str(g))
                GPIO.setup(g, GPIO.OUT)

                if self.getConfigValue(h, "inverted", False):
                    app.logger.warning("SETUP INVERTED")
                    GPIO.output(g, GPIO.HIGH)
                else:
                    app.logger.warning("SETUP NOT INVERTED")
                    GPIO.output(g, GPIO.LOW)

            app.brewapp_gpio = True
            self.state = True
            app.logger.info("ALL GPIO INITIALIZED")

        except Exception as e:
            app.logger.error("SETUP GPIO FAILD " + str(e))
            app.brewapp_gpio = False
            self.state = False

    def cleanup(self):
        try:
            GPIO.cleanup()
        except Exception as e:
            app.logger.error("CLEAN UP OF GPIO FAILD " + str(e))

    def getDevices(self):
        return ['U13_{}'.format(u) for u in range(19, 35)]

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))
        if not app.brewapp_gpio:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(device))
            return

        switch_name = self.getConfigValue(device, "switch", None)
        if switch_name is None:
            app.logger.warning("SWITCH NOT FOUND IN CONFIG")

        if self.getConfigValue(device, "inverted", False):
            app.logger.warning("SWITCH ON - Inverted")
            GPIO.output(switch_name, GPIO.LOW)
        else:
            app.logger.warning("SWITCH ON - Not Inverted")
            GPIO.output(switch_name, GPIO.HIGH)

    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
        if not app.brewapp_gpio:
            app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(device))
            return

        switch_name = self.getConfigValue(device, "switch", None)
        if switch_name is None:
            app.logger.warning("SWITCH NOT FOUND IN CONFIG")

        if self.getConfigValue(device, "inverted", False):
            app.logger.warning("SWITCH OFF - Inverted")
            GPIO.output(switch_name, GPIO.HIGH)
        else:
            app.logger.warning("SWITCH OFF - Not Inverted")
            GPIO.output(switch_name, GPIO.LOW)
