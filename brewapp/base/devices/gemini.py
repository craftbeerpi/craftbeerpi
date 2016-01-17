import subprocess
from brewapp.hardwarebase import HardwareBase
class Gemini(HardwareBase):

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
        try:
            id = translateDeviceName(device)
            command = "sudo sispmctl -o " + str(id)
            subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
        except Exception as e:
            app.logger.error("Can't switch on Socket:" + str(id) + "; ERROR: " + str(e))
        pass

    def switchOFF(self, device):

        try:
            id = translateDeviceName(device)
            command = "sudo sispmctl -f " + str(id)
            subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
        except Exception as e:
            app.logger.error("Can't switch off Socket:" + str(id) + "; ERROR: " + str(e))
        pass
