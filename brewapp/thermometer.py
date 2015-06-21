import globalprops
from subprocess import Popen, PIPE, call

## Method to read the temperatur
def tempData1Wire(tempSensorId):
    
    ## Test Moe
    if globalprops.gpioMode == False or globalprops.testMode == True:
        pipe = Popen(["cat","w1_slave"], stdout=PIPE)
    ## GPIO Mode
    else:
        pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + globalprops.tempSensorId + "/w1_slave"], stdout=PIPE)
    
    result = pipe.communicate()[0]

    ## part the file
    if (result.split('\n')[0].split(' ')[11] == "YES"):
        temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
    else:
        temp_C = -99 #bad temp reading
      
    return temp_C