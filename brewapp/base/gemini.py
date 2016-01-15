
class Gemini(object):

    def init(self):
        pass

    def getDevices(self):
        gpio = []
        for i in range(1, 6):
            gpio.append("SOCKET"+str(i))
        return gpio

    def switchON(self, device):

        print "#### GEMINI ON", device
        pass

    def switchOFF(self, device):
        print "#### GEMINI OFF", device
        pass
