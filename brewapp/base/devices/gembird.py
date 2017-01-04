import subprocess
from brewapp.base.actor import ActorBase
from brewapp import app
class GembirdUSB(ActorBase):

    def init(self):
        self.state = True

    def getDevices(self):
        gpio = []
        for i in range(1, 5):
            gpio.append("SOCKET"+str(i))
        return gpio
    def translateDeviceName(self, name):
        if(name == None or name == ""):
            return None
        return int(name[6:])

    def switchON(self, device):
        try:
            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            no = self.translateDeviceName(switch_name)
            command = "sudo sispmctl -o " + str(no)
            subprocess.call(command, shell=True)
            self.isSwitchOn(device)
        except Exception as e:
            app.logger.error("Can't switch on Socket:" + str(no) + "; ERROR: " + str(e))

    def switchOFF(self, device):
        try:
            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            no = self.translateDeviceName(switch_name)
            command = "sudo sispmctl -f " + str(no)
            subprocess.call(command, shell=True)
            self.isSwitchOn(device)
        except Exception as e:
            app.logger.error("Can't switch off Socket:" + str(no) + "; ERROR: " + str(e))

    def isSwitchOn(self, device):
        try:
            switch_name = self.getConfigValue(device, "switch", None)
            if switch_name is None:
                app.logger.warning("SWITCH NOT FOUND IN CONFIG")
                pass

            no = self.translateDeviceName(switch_name)
            command = "sudo sispmctl -nqg " + str(no)
            switchState = subprocess.check_output(command, shell=True)
            if (int(switchState) == int(0)):
                app.logger.info("Switch " + str(no) + " is off!")
                return False
            else:
                app.logger.info("Switch " + str(no) + " is on!")
                return True
        except Exception as e:
            app.logger.error("Can't get switch state Socket:" + str(no) + "; ERROR: " + str(e))
