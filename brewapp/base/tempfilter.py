import logging
from collections import deque


class TemperatureFilter(object):

    def __init__(self, maxViableDeviation=4):
        self._logger = logging.getLogger(type(self).__name__)
        self.__deque = deque(maxlen=5)
        self.__maxViableDeviation = maxViableDeviation
        self.__lastKnownGood = 0

    def filterTemperature(self, temperature):
        self.__deque.append(temperature)
        median = sorted(self.__deque)[len(self.__deque)//2]
        deviation = abs(median - temperature)

        self._logger.debug("deq: " + str(self.__deque))
        self._logger.debug("med: " + str(median))
        self._logger.debug("dev: " + str(deviation))

        if deviation > self.__maxViableDeviation:
            return self.__lastKnownGood
        else:
            self.__lastKnownGood = temperature
            return temperature
