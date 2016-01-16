
class PiFace(object):

    try:
        import pifacedigitalio as piface
        print "PiFace OK"
    except:
        print "PiFace ERROR"
        pass

    def init(self):
        piface.init()
        pass

    def getDevices(self):
        gpio = []
        for i in range(2, 6):
            gpio.append("GPIO"+str(i))
        return gpio

    def translateDeviceName(self, name):
        return name[4:]

    def switchON(self, device):
        piface.digital_write(gpio,1)
        pass

    def switchOFF(self, device):
        piface.digital_write(gpio,0)
        pass
