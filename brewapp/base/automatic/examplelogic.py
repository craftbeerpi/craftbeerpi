from automaticlogic import *
from brewapp import app
import time
from brewapp.base.util import *

@brewautomatic()
class CustomLogic(Automatic):

    ## Define config paramter as array of dicts
    configparameter = [{"name":"Parameter1","value":1},{"name":"Paramter2","value":"ABC"}]

    def run(self):
        ## loop for automatic
        while self.isRunning():
            ## access config paramter at runtime
            print self.config
            ## make sure to add a sleep to the while loop
            time.sleep(1)
