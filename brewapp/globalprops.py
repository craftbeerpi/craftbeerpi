from brewapp.model import db, Step, Temperatur, Log, Config, getAsArray
from Queue import Queue
## if test mode
testMode = True
###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = True
heatingState = False
agitatorState = False
autoState = False
current_step = None

#temp_cache = getAsArray(Temperatur)

temps = {
    "temp1": [0,0],
    "temp2": [0,0],
}

chart_cache =  {}

chart_queues = {
    'temps' : Queue(maxsize=0),
}

def loadData():
    temps = db.session.query(Temperatur).all()

    x = 'temp1'
    chart_cache[x] = []

    print len(temps)
    for t in temps:
        x = 'temp1'
        chart_cache[x] += [[t.to_unixTime(), t.value1]]


loadData()
