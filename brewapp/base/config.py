from brewapp import app


app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_stepaction = []
app.brewapp_gpio = False
app.testMode = False
app.brewapp_jobstate = {}
app.brewapp_current_step = None
app.brewapp_button = {"next": 23, "reset": 24}
app.brewapp_kettle_state = {}
app.brewapp_kettle = {}
app.brewapp_kettle_temps_log = {}
app.brewapp_kettle_automatic = {}
app.brewapp_pid_state =  {}
app.brewapp_pid = []

from brewapp.base.devices import *
from brewapp.base.thermometer import *
from brewapp.base.pid.overshootpid import *

## GPIO LIB
#app.brewapp_hardware = piface.PiFace()
#app.brewapp_hardware = dummygpio.DummyGPIO()
#app.brewapp_hardware = gpio.BrewGPIO()
app.brewapp_hardware = gembird.GembirdUSB()

app.brewapp_pid_logic = OvershootPID
##
app.brewapp_thermometer = w1_thermometer.OneWireThermometer()
