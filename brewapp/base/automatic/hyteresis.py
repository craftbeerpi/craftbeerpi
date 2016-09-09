from automaticlogic import *
from brewapp import app, socketio
import time
from brewapp.base.util import *

@brewautomatic()
class HysteresisLogic(Automatic):

    ## Define config paramter as array of dicts
    configparameter = [{"name":"ON","value": 0}, {"name":"OFF","value": 0}]

    def run(self):
        try:
            on = float(self.config["ON"])
        except Exception as e:
            on = 0
            app.logger.error("Wrong ON parameter for hysteresis! Set ON parameter to 0")
            socketio.emit('message', {"headline": "WRONG_HYSTERESIS_PARAMETER", "message": "WRONG_ON_PARAMETER"},
                          namespace='/brew')

        try:
            off = float(self.config["OFF"])

        except Exception as e:
            off = 0
            app.logger.error("Wrong max parameter!")
            socketio.emit('message', {"headline": "WRONG_HYSTERESIS_PARAMETER", "message": "WRONG_OFF_PARAMETER"},
                          namespace='/brew')


        while self.isRunning():
            currentTemp = self.getCurrentTemp()  ## Current temperature
            targetTemp = self.getTargetTemp()  ## Target Temperature

            if currentTemp + on < targetTemp:
                self.switchHeaterON()

            if currentTemp + off > targetTemp:
                self.switchHeaterOFF()

            socketio.sleep(1)

        self.switchHeaterOFF()
