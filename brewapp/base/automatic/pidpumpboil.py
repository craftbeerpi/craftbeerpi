import time
from brewapp import app, socketio

from automaticlogic import *
from datetime import datetime

class PID(object):
    ek_1 = 0.0
    xk_1 = 0.0
    xk_2 = 0.0

    yk = 0.0

    GMA_HLIM = 100.0
    GMA_LLIM = 0.0

    def __init__(self, ts, kc, ti, td):
        self.kc = kc
        self.ti = ti
        self.td = td
        self.ts = ts
        self.k0 = 0.0
        self.k1 = 0.0
        self.pp = 0.0
        self.pi = 0.0
        self.pd = 0.0

        if (self.ti == 0.0):
            self.k0 = 0.0
        else:
            self.k0 = self.kc * self.ts / self.ti
        self.k1 = self.kc * self.td / self.ts

    def calc(self, xk, tset):

        ek = 0.0
        ek = tset - xk # calculate e[k] = SP[k] - PV[k]

        self.pp = self.kc * (PID.xk_1 - xk) # y[k] = y[k-1] + Kc*(PV[k-1] - PV[k])
        self.pi = self.k0 * ek  # + Kc*Ts/Ti * e[k]
        self.pd = self.k1 * (2.0 * PID.xk_1 - xk - PID.xk_2)
        PID.yk += self.pp + self.pi + self.pd


        PID.xk_2 = PID.xk_1  # PV[k-2] = PV[k-1]
        PID.xk_1 = xk    # PV[k-1] = PV[k]

        # limit y[k] to GMA_HLIM and GMA_LLIM
        if (PID.yk > PID.GMA_HLIM):
            PID.yk = PID.GMA_HLIM
        if (PID.yk < PID.GMA_LLIM):
            PID.yk = PID.GMA_LLIM

        return PID.yk


@brewautomatic()
class PIDPUMPBOILLogic(Automatic):

    configparameter = [
    {"name":"P", "value":100},
    {"name":"I", "value":20},
    {"name":"D","value":5},
    {"name": "wait_time", "value":5},
    {"name": "PumpTime", "value":15},
    {"name": "PumpPause", "value":5},
    {"name": "PumpAbschalt", "value":80},
    {"name": "Boil", "value":97}]

    def run(self):
        sampleTime = 5
        wait_time = float(self.config["wait_time"])
        p = float(self.config["P"])
        i = float(self.config["I"])
        d = float(self.config["D"])
        pid = PID(wait_time,p,i,d)
        boilTemp = float(self.config["Boil"])
        pumpTime = int(self.config["PumpTime"])
        pumpPause = int(self.config["PumpPause"])
        pumpAllTime = pumpTime + pumpPause
        pumpSafety = float(self.config["PumpAbschalt"])
        pumpOn = False;
        cs = app.brewapp_current_step;
        currentTemp = self.getCurrentTemp()
        if(currentTemp < pumpSafety):
            if(not pumpOn):
                self.switchAgitatorON()
            pumpOn = True
        else:
            if(pumpOn):
                self.switchAgitatorOFF()
            pumpOn = False


        while self.isRunning():
			if(self.getTargetTemp()<boilTemp):
				heat_percent = pid.calc(self.getCurrentTemp(), self.getTargetTemp())
				heating_time = sampleTime * heat_percent / 100
				wait_time = sampleTime - heating_time
        currentTemp = self.getCurrentTemp()
        targetTemp = self.getTargetTemp()
        if(targetTemp > 0):
				    self.switchHeaterON()
				socketio.sleep(heating_time)
				self.switchHeaterOFF()
				socketio.sleep(wait_time)

				if(cs != app.brewapp_current_step):
					cs = app.brewapp_current_step
					currentTemp = self.getCurrentTemp()
					if(currentTemp < pumpSafety):
						if(not pumpOn):
							self.switchAgitatorON()
						pumpOn = True
					else:
						if(pumpOn):
							self.switchAgitatorOFF()
						pumpOn = False

				if(app.brewapp_current_step != None):
					currentTemp = self.getCurrentTemp() ## Current temperature
					start = app.brewapp_current_step.get("timer_start")
					if(start != None):
						end = app.brewapp_current_step.get("endunix") + app.brewapp_current_step.get("timer")*60000
						now = int((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000
						toEnd = (end-now)/60/1000
						fromStart = app.brewapp_current_step.get("timer") - toEnd - 1;
						mod = fromStart % pumpAllTime
						print str(mod)
						if(mod < pumpTime):
							currentTemp = self.getCurrentTemp()
							if(currentTemp < pumpSafety):
								if(not pumpOn):
									self.switchAgitatorON()
								pumpOn = True
							else:
								if(pumpOn):
									self.switchAgitatorOFF()
								pumpOn = False
						else:
							if(pumpOn):
								self.switchAgitatorOFF()
							pumpOn = False
			else:
				self.switchHeaterON()
				socketio.sleep(1)

	##Switch off when finished
	self.switchHeaterOFF()				
