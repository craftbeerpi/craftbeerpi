from automaticlogic import *
from brewapp import app, socketio
import time
from brewapp.base.util import *

@brewautomatic()
class OvershootLogic_by_Norn(Automatic):

    ## Define config paramter as array of dicts
    configparameter = [{"name":"Overshoot","value":0}]

    state = False
    setpoint = 0

    def run(self):

        try:
            overshoot = float(self.config["Overshoot"])
        except Exception as e:
            app.logger.error("Wrong overshoot parameter! Set overshoot parameter to 0")
            overshoot = 0

        while self.isRunning():
            currentTemp = self.getCurrentTemp() ## Current temperature
            targetTemp = self.getTargetTemp() ## Target Temperature
            ## Current Temp is below Target Temp ... overshoot is on ...  switch heater on
            if(currentTemp + overshoot < targetTemp and self.state == False and targetTemp != self.setpoint):
                self.state = True
                self.switchHeaterON()
            ## Switch overshoot off if target temp is reached
            if(currentTemp >= targetTemp):
                self.setpoint = targetTemp
            ## Current Temp is below Target Temp ... overshoot is off ...  switch heater on
            if(currentTemp < targetTemp and self.state == False and targetTemp == self.setpoint):
                self.state = True
                self.switchHeaterON()
            ## Current Temp is equal or higher than Target Temp ... overshoot is on ... switch Heater off
            if(currentTemp + overshoot >= targetTemp and self.state == True and targetTemp != self.setpoint):
                self.state = False
                self.switchHeaterOFF()
            ## Current Temp is equal or higher than Target Temp ... overshoot is off ... switch Heater off
            if(currentTemp >= targetTemp and self.state == True and targetTemp == self.setpoint):
                self.state = False
                self.switchHeaterOFF()
            socketio.sleep(1)

        self.switchHeaterOFF()
        app.logger.info("Stop PID - Kettle Id: "+ str(self.kid))
