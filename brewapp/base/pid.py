import time
from thread import start_new_thread
from brewapp import app, socketio, db
from gpio import *


## STOP PID Controller
def stopPID(vid):
    key = str(vid)+"pid";
    app.brewapp_kettle_automatic[key] = False

## START PID Controller
def startPID(vid):
    key = str(vid)+"pid"
    app.brewapp_kettle_automatic[key] = True
    if(app.brewapp_automatic_logic == "overshoot"):
        start_new_thread(pidjob,(vid,))
    else:
        start_new_thread(pidjob2,(vid,))

def getCurrentTemp(kid):
    return app.brewapp_kettle_state[kid]["temp"]

def getTargetTemp(kid):
    return app.brewapp_kettle_state[kid]["target_temp"]

def switchHeaterON(kid):
    switchON(app.brewapp_kettle_state[kid]["heater"]["gpio"])
    app.brewapp_kettle_state[kid]["heater"]["state"] = True

def switchHeaterOFF(kid):
    switchOFF(app.brewapp_kettle_state[kid]["heater"]["gpio"])
    app.brewapp_kettle_state[kid]["heater"]["state"] = False

def isRunning(kid):
    key = str(kid)+"pid"
    return app.brewapp_kettle_automatic[key]

## PID LOGIC IT SELF
## Place your custom code into the while loop

def pidjob(kid):
    app.logger.info("Start Overshoot - Kettle Id: "+ str(kid))
    while isRunning(kid):
        ## Current temperature
        currentTemp =  getCurrentTemp(kid)
        ## Target Temperature
        targetTemp = getTargetTemp(kid)

        ## Current Temp is below Target Temp ... switch heater on
        if(currentTemp < targetTemp - app.brewapp_pid_overshoot and app.brewapp_pid_state.get(kid, False) == False):
            app.brewapp_pid_state[kid] = True
            switchHeaterON(kid)
            socketio.emit('kettle_automatic_on', kid, namespace ='/brew')
        ## Current Temp is equal or higher than Target Temp ... switch Heater off
        if(currentTemp >= targetTemp - app.brewapp_pid_overshoot and app.brewapp_pid_state.get(kid, False) == True):
            app.brewapp_pid_state[kid] = False
            switchHeaterOFF(kid)
            socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
        time.sleep(1)

    app.brewapp_pid_state[kid] = False
    switchHeaterOFF(kid)
    socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
    app.logger.info("Stop Overshoot - Kettle Id: "+ str(kid))


def pidjob2(kid):
    app.logger.info("Start PID - Kettle Id: "+ str(kid))

    pid = pidpy(app.brewapp_pid_interval,app.brewapp_p,app.brewapp_i,app.brewapp_d)

    while isRunning(kid):
        ## Current temperature
        currentTemp =  getCurrentTemp(kid)
        ## Target Temperature
        targetTemp = getTargetTemp(kid)

        heat_percent = pid.calcPID_reg4(currentTemp, targetTemp, True)
        heating_time = app.brewapp_pid_interval * heat_percent / 100
        wait_time = app.brewapp_pid_interval - heating_time
        print heating_time
        print wait_time
        ## HEATING ON
        switchHeaterON(kid)
        socketio.emit('kettle_automatic_on', kid, namespace ='/brew')
        time.sleep(heating_time)
        ## HEATING OFF
        switchHeaterOFF(kid)
        socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
        time.sleep(wait_time)
        print "WAIT"


    app.brewapp_pid_state[kid] = False
    switchHeaterOFF(kid)
    socketio.emit('kettle_automatic_off', kid, namespace ='/brew')
    app.logger.info("Stop PID - Kettle Id: "+ str(kid))


class pidpy(object):
    ek_1 = 0.0  # e[k-1] = SP[k-1] - PV[k-1] = Tset_hlt[k-1] - Thlt[k-1]
    ek_2 = 0.0  # e[k-2] = SP[k-2] - PV[k-2] = Tset_hlt[k-2] - Thlt[k-2]
    xk_1 = 0.0  # PV[k-1] = Thlt[k-1]
    xk_2 = 0.0  # PV[k-2] = Thlt[k-1]
    yk_1 = 0.0  # y[k-1] = Gamma[k-1]
    yk_2 = 0.0  # y[k-2] = Gamma[k-1]
    lpf_1 = 0.0 # lpf[k-1] = LPF output[k-1]
    lpf_2 = 0.0 # lpf[k-2] = LPF output[k-2]

    yk = 0.0 # output

    GMA_HLIM = 100.0
    GMA_LLIM = 0.0

    def __init__(self, ts, kc, ti, td):
        self.kc = kc
        self.ti = ti
        self.td = td
        self.ts = ts
        self.k_lpf = 0.0
        self.k0 = 0.0
        self.k1 = 0.0
        self.k2 = 0.0
        self.k3 = 0.0
        self.lpf1 = 0.0
        self.lpf2 = 0.0
        self.ts_ticks = 0
        self.pid_model = 3
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

    def calcPID_reg3(self, xk, tset, enable):
        ek = 0.0
        lpf = 0.0
        ek = tset - xk # calculate e[k] = SP[k] - PV[k]
        #--------------------------------------
        # Calculate Lowpass Filter for D-term
        #--------------------------------------
        lpf = self.lpf1 * pidpy.lpf_1 + self.lpf2 * (ek + pidpy.ek_1);

        if (enable):
            #-----------------------------------------------------------
            # Calculate PID controller:
            # y[k] = y[k-1] + kc*(e[k] - e[k-1] +
            # Ts*e[k]/Ti +
            # Td/Ts*(lpf[k] - 2*lpf[k-1] + lpf[k-2]))
            #-----------------------------------------------------------
            self.pp = self.kc * (ek - pidpy.ek_1) # y[k] = y[k-1] + Kc*(PV[k-1] - PV[k])
            self.pi = self.k0 * ek  # + Kc*Ts/Ti * e[k]
            self.pd = self.k1 * (lpf - 2.0 * pidpy.lpf_1 + pidpy.lpf_2)
            pidpy.yk += self.pp + self.pi + self.pd
        else:
            pidpy.yk = 0.0
            self.pp = 0.0
            self.pi = 0.0
            self.pd = 0.0

        pidpy.ek_1 = ek # e[k-1] = e[k]
        pidpy.lpf_2 = pidpy.lpf_1 # update stores for LPF
        pidpy.lpf_1 = lpf

        # limit y[k] to GMA_HLIM and GMA_LLIM
        if (pidpy.yk > pidpy.GMA_HLIM):
            pidpy.yk = pidpy.GMA_HLIM
        if (pidpy.yk < pidpy.GMA_LLIM):
            pidpy.yk = pidpy.GMA_LLIM

        return pidpy.yk

    def calcPID_reg4(self, xk, tset, enable):

        ek = 0.0
        ek = tset - xk # calculate e[k] = SP[k] - PV[k]

        if (enable):
            #-----------------------------------------------------------
            # Calculate PID controller:
            # y[k] = y[k-1] + kc*(PV[k-1] - PV[k] +
            # Ts*e[k]/Ti +
            # Td/Ts*(2*PV[k-1] - PV[k] - PV[k-2]))
            #-----------------------------------------------------------
            self.pp = self.kc * (pidpy.xk_1 - xk) # y[k] = y[k-1] + Kc*(PV[k-1] - PV[k])
            self.pi = self.k0 * ek  # + Kc*Ts/Ti * e[k]
            self.pd = self.k1 * (2.0 * pidpy.xk_1 - xk - pidpy.xk_2)
            pidpy.yk += self.pp + self.pi + self.pd
        else:
            pidpy.yk = 0.0
            self.pp = 0.0
            self.pi = 0.0
            self.pd = 0.0

        pidpy.xk_2 = pidpy.xk_1  # PV[k-2] = PV[k-1]
        pidpy.xk_1 = xk    # PV[k-1] = PV[k]

        # limit y[k] to GMA_HLIM and GMA_LLIM
        if (pidpy.yk > pidpy.GMA_HLIM):
            pidpy.yk = pidpy.GMA_HLIM
        if (pidpy.yk < pidpy.GMA_LLIM):
            pidpy.yk = pidpy.GMA_LLIM

        return pidpy.yk
