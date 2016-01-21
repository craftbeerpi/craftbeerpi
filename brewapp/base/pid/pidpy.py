import time
#from brewapp.base.pid.pidbase import *
from pidbase import *

class pidpy(PIDBase):

    xk_1 = 0.0  # PV[k-1] = Thlt[k-1]
    xk_2 = 0.0  # PV[k-2] = Thlt[k-1]
    yk = 0.0 # output

    GMA_HLIM = 100.0
    GMA_LLIM = 0.0
    def __init__(self, kid, ts=5, kc=44, ti=165, td=4):
        self.kid = kid
        self.kc = kc
        self.ti = ti
        self.td = td
        self.ts = ts
        self.k_lpf = 0.0
        self.k0 = 0.0
        self.k1 = 0.0
        self.lpf1 = 0.0
        self.lpf2 = 0.0
        self.ts_ticks = 0
        self.pp = 0.0
        self.pi = 0.0
        self.pd = 0.0
        if (self.ti == 0.0):
            self.k0 = 0.0
        else:
            self.k0 = self.kc * self.ts / self.ti
        self.k1 = self.kc * self.td / self.ts
        self.lpf1 = (2.0 * self.k_lpf - self.ts) / (2.0 * self.k_lpf + self.ts)
        self.lpf2 = self.ts / (2.0 * self.k_lpf + self.ts)


    def calcPID_reg4(self, xk, tset, enable):
        ek = 0.0
        ek = tset - xk
        if (enable):
            self.pp = self.kc * (pidpy.xk_1 - xk)
            self.pi = self.k0 * ek
            self.pd = self.k1 * (2.0 * pidpy.xk_1 - xk - pidpy.xk_2)
            pidpy.yk += self.pp + self.pi + self.pd
        else:
            pidpy.yk = 0.0
            self.pp = 0.0
            self.pi = 0.0
            self.pd = 0.0

        pidpy.xk_2 = pidpy.xk_1
        pidpy.xk_1 = xk

        if (pidpy.yk > pidpy.GMA_HLIM):
            pidpy.yk = pidpy.GMA_HLIM
        if (pidpy.yk < pidpy.GMA_LLIM):
            pidpy.yk = pidpy.GMA_LLIM

        return pidpy.yk

    def run(self):

        setpoint = 25
        enable = True
        sampleTime = 5

        while self.isRunning():
            heat_percent = self.calcPID_reg4(self.getCurrentTemp(), self.getTargetTemp(), True)
            heating_time = sampleTime * heat_percent / 100
            wait_time = sampleTime - heating_time
            self.switchHeaterON()
            time.sleep(heating_time)
            self.switchHeaterOFF()
            time.sleep(wait_time)
