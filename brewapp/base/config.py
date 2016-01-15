from brewapp import app
from newgpio import *

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


app.brewapp_hardware = GPIO()
