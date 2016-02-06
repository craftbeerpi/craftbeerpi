from brewapp.base.pid.pidbase import *
from brewapp import app
import time

@brewautomatic()
class CustomLogic2(PIDBase):

    configparameter = [
    {"name":"overshoot","value":22},
    {"name":"overshoot1","value":22},
    {"name":"overshoot2","value":22},
    {"name":"overshoot3","value":22},
    ]

    state = False
    def run(self):


        while self.isRunning():
            print self.config
            time.sleep(1)

        self.switchHeaterOFF()
        app.logger.info("Stop PID - Kettle Id: "+ str(self.kid))
