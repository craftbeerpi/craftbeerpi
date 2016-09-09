from automaticlogic import *
from brewapp import app, socketio
import time
from brewapp.base.util import *

@brewautomatic()
class OvershootLogic(Automatic):

    ## Define config paramter as array of dicts
    configparameter = [{"name":"Overshoot","value": 0}]

    state = False

    def run(self):


        try:
            overshoot = float(self.config["Overshoot"])
        except Exception as e:
            app.logger.error("Wrong overshoot parameter! Set overshoot parameter to 0")
            overshoot = 0

        while self.isRunning():
            currentTemp = self.getCurrentTemp() ## Current temperature
            targetTemp = self.getTargetTemp() ## Target Temperature

            if(currentTemp == None):
                socketio.sleep(1)
                return

            ## Current Temp is below Target Temp ... switch heater on
            if(currentTemp + overshoot < targetTemp and self.state == False):
                self.state = True
                self.switchHeaterON()
            ## Current Temp is equal or higher than Target Temp ... switch Heater off
            if(currentTemp + overshoot >= targetTemp and self.state == True):
                self.state = False
                self.switchHeaterOFF()
            socketio.sleep(1)

        self.switchHeaterOFF()
        app.logger.info("Stop PID - Kettle Id: "+ str(self.kid))
