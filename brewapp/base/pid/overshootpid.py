from brewapp.base.pid.pidbase import *
from brewapp import app
import time

class OvershootPID(PIDBase):
    state = False
    def run(self):
        
        while self.isRunning():
            currentTemp = self.getCurrentTemp() ## Current temperature
            targetTemp = self.getTargetTemp() ## Target Temperature
            ## Current Temp is below Target Temp ... switch heater on
            if(currentTemp < targetTemp and self.state == False):
                self.state = True
                self.switchHeaterON()
            ## Current Temp is equal or higher than Target Temp ... switch Heater off
            if(currentTemp >= targetTemp and self.state == True):
                self.state = False
                self.switchHeaterOFF()
            time.sleep(1)

        self.switchHeaterOFF()
        app.logger.info("Stop PID - Kettle Id: "+ str(self.kid))
