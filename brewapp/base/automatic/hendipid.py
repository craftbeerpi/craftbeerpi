import time
from automaticlogic import *


try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass


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
class HendiPID(Automatic):

    configparameter = [
    {"name":"Hendi_Power_GPIO", "value":27},
    {"name":"P", "value":40.0},
    {"name":"I", "value":140.0},
    {"name":"D","value":0},
    {"name": "ts", "value":5}
    ]

    def run(self):
        p = float(self.config["P"])
        i = float(self.config["I"])
        d = float(self.config["D"])
        ts = float(self.config["ts"])

        pid = PID(ts,p,i,d)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.config["Hendi_Power_GPIO"],GPIO.OUT)
        pwm=GPIO.PWM(self.config["Hendi_Power_GPIO"],100)
        pwm.start(0)

        while self.isRunning():
            heat_percent = pid.calc(self.getCurrentTemp(), self.getTargetTemp())
            pwm.ChangeDutyCycle(heat_percent)
            if heat_percent == 0:
                self.switchHeaterOFF()
            else:
                self.switchHeaterON()

            socketio.sleep(ts)

        self.switchHeaterOFF()
        pwm.ChangeDutyCycle(0)
