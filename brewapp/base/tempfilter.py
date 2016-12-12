from collections import deque
import statistics as stat


class TemperatureFilter(object):

    def __init__(self, maxViableDeviation=4):
        self.__deque = deque(maxlen=5)
        self.__maxViableDeviation = maxViableDeviation
        self.__lastKnownGood = 0

    def filterTemperature(self, temperature):
        self.__deque.append(temperature)
        median = stat.median(self.__deque)
        deviation = abs(median - temperature)

        print("deq:" + str(self.__deque))
        print("med:" + str(median))
        print("dev:" + str(deviation))

        if deviation > self.__maxViableDeviation:
            return self.__lastKnownGood
        else:
            self.__lastKnownGood = temperature
            return temperature
