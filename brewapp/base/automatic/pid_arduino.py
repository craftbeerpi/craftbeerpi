import time
import logging
from brewapp import app, socketio
from automaticlogic import *


@brewautomatic()
class PIDArduinoLogic(Automatic):
    KEY_P = "P"
    KEY_I = "I"
    KEY_D = "D"
    KEY_MAXOUT = "max. output %"
    SAMPLETIME = 5

    configparameter = [
            {"name": KEY_P, "value": 107},
            {"name": KEY_I, "value": 0.9},
            {"name": KEY_D, "value": 202},
            {"name": KEY_MAXOUT, "value": 100}]

    def run(self):
        wait_time = self.SAMPLETIME
        kp = float(self.config[self.KEY_P])
        ki = float(self.config[self.KEY_I])
        kd = float(self.config[self.KEY_D])
        maxout = float(self.config[self.KEY_MAXOUT])
        pid = PIDArduino(self.SAMPLETIME, kp, ki, kd, 0, maxout)

        while self.isRunning():
            heat_percent = pid.calc(self.getCurrentTemp(), self.getTargetTemp())
            heating_time = self.SAMPLETIME * heat_percent / 100
            wait_time = self.SAMPLETIME - heating_time

            if heating_time > 0:
                self.switchHeaterON()
                socketio.sleep(heating_time)
            if wait_time > 0:
                self.switchHeaterOFF()
                socketio.sleep(wait_time)
        self.switchHeaterOFF()


# Based on Arduino PID Library
# See https://github.com/br3ttb/Arduino-PID-Library
class PIDArduino(object):
    """A proportional-integral-derivative controller.

    Args:
        sampletime (float): The interval between calc() calls.
        kp (float): Proportional coefficient.
        ki (float): Integral coefficient.
        kd (float): Derivative coefficient.
        out_min (float): Lower output limit.
        out_max (float): Upper output limit.
        time (function): A function which returns the current time in seconds.
    """

    def __init__(self, sampletime, kp, ki, kd, out_min=float('-inf'),
                 out_max=float('inf'), time=time.time):
        if kp is None:
            raise ValueError('kp must be specified')
        if ki is None:
            raise ValueError('ki must be specified')
        if kd is None:
            raise ValueError('kd must be specified')
        if sampletime <= 0:
            raise ValueError('sampletime must be greater than 0')
        if out_min >= out_max:
            raise ValueError('out_min must be less than out_max')

        self._logger = logging.getLogger(type(self).__name__)
        self._Kp = kp
        self._Ki = ki * sampletime
        self._Kd = kd / sampletime
        self._sampletime = sampletime * 1000
        self._out_min = out_min
        self._out_max = out_max
        self._integral = 0
        self._last_input = 0
        self._last_output = 0
        self._last_calc_timestamp = 0
        self._time = time

    def calc(self, input_val, setpoint):
        """Adjusts and holds the given setpoint.

        Args:
            input_val (float): The input value.
            setpoint (float): The target value.

        Returns:
            A value between `out_min` and `out_max`.
        """
        now = self._time() * 1000

        if (now - self._last_calc_timestamp) < self._sampletime:
            return self._last_output

        # Compute all the working error variables
        error = setpoint - input_val
        input_diff = input_val - self._last_input

        # In order to prevent windup, only integrate if the process is not saturated
        if self._last_output < self._out_max and self._last_output > self._out_min:
            self._integral += self._Ki * error
            self._integral = min(self._integral, self._out_max)
            self._integral = max(self._integral, self._out_min)

        p = self._Kp * error
        i = self._integral
        d = -(self._Kd * input_diff)

        # Compute PID Output
        self._last_output = p + i + d
        self._last_output = min(self._last_output, self._out_max)
        self._last_output = max(self._last_output, self._out_min)

        # Log some debug info
        self._logger.debug('P: {0}'.format(p))
        self._logger.debug('I: {0}'.format(i))
        self._logger.debug('D: {0}'.format(d))
        self._logger.debug('output: {0}'.format(self._last_output))

        # Remember some variables for next time
        self._last_input = input_val
        self._last_calc_timestamp = now
        return self._last_output
