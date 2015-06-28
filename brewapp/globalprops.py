from brewapp.model import db, Step, Temperatur, Log, Config, getAsArray
## if test mode
testMode = True
###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = False
heatingState = False
agitatorState = False
pidState = False
current_temp = 0.0
heatLog = []
temp_cache = getAsArray(Temperatur)

