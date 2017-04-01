import time
from brewapp import app, socketio

from automaticlogic import *

@brewautomatic()
class PWM(Automatic):

    configparameter = [
    {"name":"Duty Cycle(%)", "value":50},
	{"name":"Period(s)", "value":10},
	{"name":"Use Temp Setpoint As Duty Cycle","value":0}]
	

    def run(self):
	period = float(self.config["Period(s)"])
	dutycycle = float(self.config["Duty Cycle(%)"])
        
    	while self.isRunning():
		if float(self.config["Use Temp Setpoint As Duty Cycle"]) == 0:
			heating_time = period * dutycycle / 100
		else:
			temp_setpoint = self.getTargetTemp()
			if temp_setpoint > 100:
				temp_setpoint = 100
			elif temp_setpoint < 0:
				temp_setpoint = 0
				
			heating_time = period * temp_setpoint / 100
			
		wait_time = period - heating_time
        	self.switchHeaterON()
        	socketio.sleep(heating_time)
        	self.switchHeaterOFF()
        	socketio.sleep(wait_time)
   
        self.switchHeaterOFF()
