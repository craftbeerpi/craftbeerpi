
class Gemini(object):

    def init(self):
        pass

    def getDevices(self):
        gpio = []
        for i in range(1, 6):
            gpio.append("SOCKET"+str(i))
        return gpio

    def translateDeviceName(self, name):
        return name[4:]

    def switchON(self, device):

        print "#### GEMINI ON", device
        command = "sudo sispmctl -o " + str(gpio)
        subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
        pass

    def switchOFF(self, device):
        print "#### GEMINI OFF", device
        pass
