## if test mode
testMode = False

### File name of sensor file
## /sys/bus/w1/devices/<temp_sensor_id>
tempSensorId = '28-03146215acff'

### GPIO Number for Heating
heating_pin = 17

## GPIO Number Agitator
agitator_pin = 18

## interval in which the new temperatur is read
temp_db_interval = 5

## heating interval in seconds
pid_interval = 5

## PID tuning parameter
pipP=102

pidI=100

pidD=5

## hysteresis parameter in degrees celsius
## For exmpale. If current temperatur is more than 2 degrees below the traget temp turn the heating 100% on
hysteresis_min=4



###################################################################
#### INTERNAL DO NOT CHANGE PARAMETERS BELOW
gpioMode = False
heatingState = False
agitatorState = False
pidState = False
