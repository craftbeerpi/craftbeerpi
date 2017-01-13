#This module implements PWM control to emulate a % of element heat

#Duty Cycle 1 is the percentage of time the element will heat in cycle 1
#Period 1 is the total time in seconds for each cycle in DC1
#Temp from target to start DC 2 is the number of degrees below the target temp
#  at which the system will switch from DC1 to DC 2
#Duty Cycle 2 is the percentage of time the element will heat in cycle 2
#Period 2 is the total time in seconds for each cycle in DC2

#Special thanks to schrod

import time
from brewapp import app, socketio

from automaticlogic import *

@brewautomatic()
class PWM_Step_Up(Automatic):

   configparameter = [
      {"name":"Duty Cycle 1 (%)", "value":100},
      {"name":"Period (seconds) for DC 1", "value":1},
      {"name":"Temp from target to start DC 2", "value":2},
      {"name":"Duty Cycle 2 (%)", "value":50},
      {"name":"Period (seconds) for DC 2", "value":1}]

   def run(self):
      temp_difference = float(self.config["Temp from target to start DC 2"])
      dutycycle1 = float(self.config["Duty Cycle 1 (%)"])
      period1 = float(self.config["Period (seconds) for DC 1"])
      dutycycle2 = float(self.config["Duty Cycle 2 (%)"])
      period2 = float(self.config["Period (seconds) for DC 2"])

      while self.isRunning():
         current_temp = self.getCurrentTemp()
         temp_setpoint = self.getTargetTemp()

         heating_time1 = period1 * dutycycle1 / 100
         wait_time1 = period1 - heating_time1
         heating_time2 = period2 * dutycycle2 / 100
         wait_time2 = period2 - heating_time2

         if current_temp < (temp_setpoint - temp_difference):
            self.switchHeaterON()
            socketio.sleep(heating_time1)
            self.switchHeaterOFF()
            socketio.sleep(wait_time1)
         else:
            self.switchHeaterON()
            socketio.sleep(heating_time2)
            self.switchHeaterOFF()
            socketio.sleep(wait_time2)

      self.switchHeaterOFF()
