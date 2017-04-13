from automaticlogic import *
from brewapp import app
import time
from brewapp.base.util import *
from brewapp import app, socketio
from brewapp.base import buzzer
import datetime
import math

@brewautomatic()
class ThiagoLogic(Automatic):

    # Define config paramter as array of dicts
    configparameter = [{"name" : "PumpGPIO" , "value" : 17}]
    previousAlarm = datetime.datetime.now()
    lastTargetAchieved = 0

    def run(self):
        # loop for automatic
        while self.isRunning():
            currentTemp = self.getCurrentTemp()  ## Current temperature
            targetTemp = self.getTargetTemp()  ## Target Temperature

            if currentTemp < targetTemp:
                self.switchHeaterON()

            if currentTemp > targetTemp:
                self.switchHeaterOFF()

            diffTemp = math.fabs(currentTemp - targetTemp)

            # before achieve the target we just need to know when turn off the heater
            if not self.isTargetAchieved():
                # not close to target, nothing to check
                if diffTemp > 4:
                    diffTemp = 0
                else:
                    diffTemp = 4 - diffTemp

            # more and more often as faraway of target
            interval = self.getAlarmInterval(diffTemp)
            self.alarm(0.1, interval)
            
            socketio.sleep(1)

        self.switchHeaterOFF()
        self.alarm(0.1, 0)
    
    def isTargetAchieved(self):
        if self.getTargetTemp() == self.lastTargetAchieved:
            return True
        elif self.getCurrentTemp() >= self.getTargetTemp():
            self.lastTargetAchieved = self.getTargetTemp()
            self.alarm(3, 0)
            return True
        else:
            return False

    def getAlarmInterval(self, diffTemp):
        if diffTemp < 1:
            return 30
        elif diffTemp < 2:
            return 4
        elif diffTemp <= 3:
            return 2
        else:
            return 1

    def alarm(self, duration, interval):
        
        sound = ["H", duration, "L"]
        
        nextAlarm = self.previousAlarm + datetime.timedelta(seconds=interval)
        currentTime = datetime.datetime.now()

        if nextAlarm < currentTime:
            self.previousAlarm = currentTime
            buzzer.playSound(sound)

