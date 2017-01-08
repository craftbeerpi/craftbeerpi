import time
from automaticlogic import *

try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass


@brewautomatic()
class HendiPowerCtrl(Automatic):

    configparameter = [
    {"name":"Hendi_Power_GPIO", "value":27},
    ]

    def run(self):
        sampleTime = 5
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.config["Hendi_Power_GPIO"],GPIO.OUT)
        pwm=GPIO.PWM(self.config["Hendi_Power_GPIO"],100)
        pwm.start(0)

        while self.isRunning():
            heat_percent = self.getTargetTemp()
            pwm.ChangeDutyCycle(heat_percent)
            if heat_percent == 0:
                self.switchHeaterOFF()
            else:
                self.switchHeaterON()

            socketio.sleep(sampleTime)

        self.switchHeaterOFF()
        pwm.ChangeDutyCycle(0)
