from brewapp.model import db, Step, Temperatur, Log, Config, getAsArray
from Queue import Queue
## if test mode
testMode = False
###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = True
heatingState = False
agitatorState = False
pidState = False
current_step = None

temp_cache = getAsArray(Temperatur)

temps = {
    "temp1": [0,0],
    "temp2": [0,0],
}

chart_cache =  {}

chart_queues = {
    'temps' : Queue(maxsize=0),
}
