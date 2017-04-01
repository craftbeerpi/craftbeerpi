import logging
from collections import deque


class TemperatureFilter(object):

    def __init__(self, maxViableDeviation=4):
        self._logger = logging.getLogger(type(self).__name__)
        self._deque = deque(maxlen=5)
        self._maxViableDeviation = maxViableDeviation
        self._lastKnownGood = 0

    def filterTemperature(self, temperature):
        self._deque.append(temperature)
        median = sorted(self._deque)[len(self._deque)//2]
        deviation = abs(median - temperature)

        self._logger.debug("deq: " + str(self._deque))
        self._logger.debug("med: " + str(median))
        self._logger.debug("dev: " + str(deviation))

        if deviation > self._maxViableDeviation:
            return self._lastKnownGood
        else:
            self._lastKnownGood = temperature
            return temperature
