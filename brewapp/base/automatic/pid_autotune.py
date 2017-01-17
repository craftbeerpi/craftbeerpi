import time
import math
import logging
import io
from collections import deque
from collections import namedtuple
from brewapp import app, socketio
from automaticlogic import *


@brewautomatic()
class PIDAutotuneLogic(Automatic):
    KEY_OUTSTEP = "output step %"
    KEY_MAXOUT = "max. output %"
    KEY_LOOKBACK = "lookback seconds"

    configparameter = [
            {"name": KEY_OUTSTEP, "value": 100},
            {"name": KEY_MAXOUT, "value": 100},
            {"name": KEY_LOOKBACK, "value": 30}]

    def run(self):
        sampleTime = 5
        wait_time = 5
        outstep = float(self.config[self.KEY_OUTSTEP])
        outmax = float(self.config[self.KEY_MAXOUT])
        lookbackSec = float(self.config[self.KEY_LOOKBACK])
        setpoint = self.getTargetTemp()
        atune = PIDAutotune(setpoint, outstep, sampleTime, lookbackSec, 0, outmax)

        while self.isRunning() and not atune.run(self.getCurrentTemp()):
            heat_percent = atune.output
            heating_time = sampleTime * heat_percent / 100
            wait_time = sampleTime - heating_time
            self.switchHeaterON()
            socketio.sleep(heating_time)
            self.switchHeaterOFF()
            socketio.sleep(wait_time)

        app.brewapp_kettle_state[self.kid]["automatic"] = False
        stopPID(self.kid)
        socketio.emit('kettle_state_update', app.brewapp_kettle_state, namespace ='/brew')

        if atune.state == atune.STATE_SUCCEEDED:
            with io.FileIO('pidparams.txt', 'w') as file:
                for rule in atune.tuningRules:
                    params = atune.getPIDParameters(rule)
                    file.write('rule: {0}\n'.format(rule))
                    file.write('P: {0}\n'.format(params.Kp))
                    file.write('I: {0}\n'.format(params.Ki))
                    file.write('D: {0}\n\n'.format(params.Kd))


# Based on a fork of Arduino PID AutoTune Library
# See https://github.com/t0mpr1c3/Arduino-PID-AutoTune-Library
class PIDAutotune(object):
    PIDParams = namedtuple('PIDParams', ['Kp', 'Ki', 'Kd'])

    PEAK_AMPLITUDE_TOLERANCE = 0.05
    STATE_OFF = 'off'
    STATE_RELAY_STEP_UP = 'relay step up'
    STATE_RELAY_STEP_DOWN = 'relay step down'
    STATE_SUCCEEDED = 'succeeded'
    STATE_FAILED = 'failed'

    _tuning_rules = {
        # rule: [Kp_divisor, Ki_divisor, Kd_divisor]
        "ziegler-nichols": [34, 40, 160],
        "tyreus-luyben": [44,  9, 126],
        "ciancone-marlin": [66, 88, 162],
        "pessen-integral": [28, 50, 133],
        "some-overshoot": [60, 40,  60],
        "no-overshoot": [100, 40,  60],
        "brewing": [2.5, 3, 3600]
    }

    def __init__(self, setpoint, outputstep=10, sampleTimeSec=5, lookbackSec=60,
                 outputMin=float('-inf'), outputMax=float('inf'), noiseband=0.5, getTimeMs=None):
        if setpoint is None:
            raise ValueError('setpoint must be specified')
        if outputstep < 1:
            raise ValueError('outputstep must be greater or equal to 1')
        if sampleTimeSec < 1:
            raise ValueError('sampleTimeSec must be greater or equal to 1')
        if lookbackSec < sampleTimeSec:
            raise ValueError('lookbackSec must be greater or equal to sampleTimeSec')
        if outputMin >= outputMax:
            raise ValueError('outputMin must be less than outputMax')

        self._logger = logging.getLogger(type(self).__name__)
        self._inputs = deque(maxlen=round(lookbackSec / sampleTimeSec))
        self._sampleTime = sampleTimeSec * 1000
        self._setpoint = setpoint
        self._outputstep = outputstep
        self._noiseband = noiseband
        self._outputMin = outputMin
        self._outputMax = outputMax

        self._state = PIDAutotune.STATE_OFF
        self._peakTimestamps = deque(maxlen=5)
        self._peaks = deque(maxlen=5)

        self._output = 0
        self._lastRunTimestamp = 0
        self._peakType = 0
        self._peakCount = 0
        self._initialOutput = 0
        self._inducedAmplitude = 0
        self._Ku = 0
        self._Pu = 0

        if getTimeMs is None:
            self._getTimeMs = self._currentTimeMs
        else:
            self._getTimeMs = getTimeMs

    @property
    def state(self):
        return self._state

    @property
    def output(self):
        return self._output

    @property
    def tuningRules(self):
        return self._tuning_rules.keys()

    def getPIDParameters(self, tuningRule='ziegler-nichols'):
        divisors = self._tuning_rules[tuningRule]
        kp = self._Ku / divisors[0]
        ki = kp / (self._Pu / divisors[1])
        kd = kp * (self._Pu / divisors[2])
        return PIDAutotune.PIDParams(kp, ki, kd)

    def run(self, inputValue):
        now = self._getTimeMs()

        if (self._state == PIDAutotune.STATE_OFF
                or self._state == PIDAutotune.STATE_SUCCEEDED
                or self._state == PIDAutotune.STATE_FAILED):
            self._initTuner(inputValue, now)
        elif (now - self._lastRunTimestamp) < self._sampleTime:
            return False

        self._lastRunTimestamp = now

        # check input and change relay state if necessary
        if (self._state == PIDAutotune.STATE_RELAY_STEP_UP
                and inputValue > self._setpoint + self._noiseband):
            self._state = PIDAutotune.STATE_RELAY_STEP_DOWN
            self._logger.debug('switched state: {0}'.format(self._state))
            self._logger.debug('input: {0}'.format(inputValue))
        elif (self._state == PIDAutotune.STATE_RELAY_STEP_DOWN
                and inputValue < self._setpoint - self._noiseband):
            self._state = PIDAutotune.STATE_RELAY_STEP_UP
            self._logger.debug('switched state: {0}'.format(self._state))
            self._logger.debug('input: {0}'.format(inputValue))

        # set output
        if (self._state == PIDAutotune.STATE_RELAY_STEP_UP):
            self._output = self._initialOutput + self._outputstep
        elif self._state == PIDAutotune.STATE_RELAY_STEP_DOWN:
            self._output = self._initialOutput - self._outputstep

        # respect output limits
        self._output = min(self._output, self._outputMax)
        self._output = max(self._output, self._outputMin)

        # identify peaks
        isMax = True
        isMin = True

        for val in self._inputs:
            isMax = isMax and (inputValue >= val)
            isMin = isMin and (inputValue <= val)

        self._inputs.append(inputValue)

        # we don't want to trust the maxes or mins until the input array is full
        if len(self._inputs) < self._inputs.maxlen:
            return False

        # increment peak count and record peak time for maxima and minima
        inflection = False

        # peak types:
        # -1: minimum
        # +1: maximum
        if isMax:
            if self._peakType == -1:
                inflection = True
            self._peakType = 1
        elif isMin:
            if self._peakType == 1:
                inflection = True
            self._peakType = -1

        # update peak times and values
        if inflection:
            self._peakCount += 1
            self._peaks.append(inputValue)
            self._peakTimestamps.append(now)
            self._logger.debug('found peak: {0}'.format(inputValue))
            self._logger.debug('peak count: {0}'.format(self._peakCount))

        # check for convergence of induced oscillation
        # convergence of amplitude assessed on last 4 peaks (1.5 cycles)
        self._inducedAmplitude = 0

        if inflection and (self._peakCount > 4):
            absMax = self._peaks[-2]
            absMin = self._peaks[-2]
            for i in range(0, len(self._peaks) - 2):
                self._inducedAmplitude += abs(self._peaks[i] - self._peaks[i+1])
                absMax = max(self._peaks[i], absMax)
                absMin = min(self._peaks[i], absMin)

            self._inducedAmplitude /= 6.0

            # check convergence criterion for amplitude of induced oscillation
            amplitudeDev = ((0.5 * (absMax - absMin) - self._inducedAmplitude)
                            / self._inducedAmplitude)

            self._logger.debug('amplitude: {0}'.format(self._inducedAmplitude))
            self._logger.debug('amplitude deviation: {0}'.format(amplitudeDev))

            if amplitudeDev < PIDAutotune.PEAK_AMPLITUDE_TOLERANCE:
                self._state = PIDAutotune.STATE_SUCCEEDED

        # if the autotune has not already converged
        # terminate after 10 cycles
        if self._peakCount >= 20:
            self._output = 0
            self._state = PIDAutotune.STATE_FAILED
            return True

        if self._state == PIDAutotune.STATE_SUCCEEDED:
            self._output = 0

            # calculate ultimate gain
            self._Ku = 4.0 * self._outputstep / (self._inducedAmplitude * math.pi)

            # calculate ultimate period in seconds
            period1 = self._peakTimestamps[3] - self._peakTimestamps[1]
            period2 = self._peakTimestamps[4] - self._peakTimestamps[2]
            self._Pu = 0.5 * (period1 + period2) / 1000.0
            return True

        return False

    def _currentTimeMs(self):
        return time.time() * 1000

    def _initTuner(self, inputValue, timestamp):
        self._peakType = 0
        self._peakCount = 0
        self._output = 0
        self._initialOutput = 0
        self._Ku = 0
        self._Pu = 0
        self._inputs.clear()
        self._peaks.clear()
        self._peakTimestamps.clear()
        self._peakTimestamps.append(timestamp)
        self._state = PIDAutotune.STATE_RELAY_STEP_UP
