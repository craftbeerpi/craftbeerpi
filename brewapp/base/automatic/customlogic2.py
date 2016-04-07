from automaticlogic import *
from brewapp import app
import time

@brewautomatic()
class CustomLogic2(Automatic):

    configparameter = [
        {"name":"Wert1","value":1},
        {"name":"Wert2","value":2},
        {"name":"Wert3","value":3}
    ]

    state = False
    def run(self):
        while self.isRunning():
            print self.config
            print app.brewapp_config["Unit"]
            time.sleep(1)

        self.switchHeaterOFF()
        app.logger.info("Stop PID - Kettle Id: "+ str(self.kid))
