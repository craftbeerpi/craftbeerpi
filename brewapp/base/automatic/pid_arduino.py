import time
from brewapp import app, socketio
from automaticlogic import *


@brewautomatic()
class PIDArduinoLogic(Automatic):

    configparameter = [
            {"name": "P", "value": 44},
            {"name": "I", "value": 165},
            {"name": "D", "value": 4},
            {"name": "wait_time", "value": 5}]

    def run(self):
        sampleTime = 5
        wait_time = float(self.config["wait_time"])
        p = float(self.config["P"])
        i = float(self.config["I"])
        d = float(self.config["D"])
        pid = PIDArduino(wait_time, p, i, d)

        while self.isRunning():
            heat_percent = pid.calc(self.getCurrentTemp(), self.getTargetTemp())
            heating_time = sampleTime * heat_percent / 100
            wait_time = sampleTime - heating_time
            self.switchHeaterON()
            socketio.sleep(heating_time)
            self.switchHeaterOFF()
            socketio.sleep(wait_time)


# Based on Arduino PID Library
# See https://github.com/br3ttb/Arduino-PID-Library
class PIDArduino(object):

    def __init__(self, kp, ki, kd, sampleTimeSec,
                 outputMin=float('-inf'), outputMax=float('inf')):
        if kp is None:
            raise ValueError('kp must be specified')
        if ki is None:
            raise ValueError('ki must be specified')
        if kd is None:
            raise ValueError('kd must be specified')
        if sampleTimeSec <= 0:
            raise ValueError('sampleTimeSec must be greater than 0')
        if outputMin >= outputMax:
            raise ValueError('outputMin must be less than outputMax')

        self._Kp = kp
        self._Ki = ki * sampleTimeSec
        self._Kd = kd / sampleTimeSec
        self._sampleTime = sampleTimeSec * 1000
        self._outputMin = outputMin
        self._outputMax = outputMax
        self._iTerm = 0
        self._lastInput = 0
        self._lastOutput = 0
        self._lastCalc = 0

    def calc(self, inputValue, setpoint):
        now = PIDArduino._currentTimeMs()

        if (now - self._lastCalc) < self._sampleTime:
            return self._lastOutput

        # Compute all the working error variables
        error = setpoint - inputValue
        self._iTerm += self._Ki * error
        self._iTerm = min(self._iTerm, self._outputMax)
        self._iTerm = max(self._iTerm, self._outputMin)
        dInput = inputValue - self._lastInput

        # Compute PID Output
        self._lastOutput = self._Kp * error + self._iTerm - self._Kd * dInput
        self._lastOutput = min(self._lastOutput, self._outputMax)
        self._lastOutput = max(self._lastOutput, self._outputMin)

        # Remember some variables for next time*/
        self._lastInput = inputValue
        self._lastCalc = now
        return self._lastOutput

    def _currentTimeMs():
        return time.time() * 1000
