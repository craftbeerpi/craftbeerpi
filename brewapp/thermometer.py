import globalprops
from brewapp.model import Config
from subprocess import Popen, PIPE, call

## Method to read the temperatur
def tempData1Wire(tempSensorId):

    if globalprops.owfsWin == True:
         pipe = Popen(["C:\\Programme\\OWFS\\bin\\owread", "-s", ":3000","/" + tempSensorId + "/temperature"], shell=False,stdout=PIPE)
    else:     
        ## Test Mode

        if (globalprops.testMode == True):
            pipe = Popen(["cat","w1_slave"], stdout=PIPE)
        ## GPIO Mode
        else:
            pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)

    result = pipe.communicate()[0]

    ## parse the file
    if globalprops.owfsWin == True: 
        temp_C = float(result)
        print str(temp_C)
    else:
       if (result.split('\n')[0].split(' ')[11] == "YES"):
           temp_C = float(result.split("=")[-1])/1000 # temp in Celcius

       else:
           temp_C = -99 #bad temp reading

    return temp_C
