from brewapp import app

app.brewapp_jobs = []
app.brewapp_init = []
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

## possible parameters are "overshoot" or "pid"
app.brewapp_automatic_logic = "overshoot"

## Simple Overshoot Logic
app.brewapp_pid_overshoot = 0

## PID Loigc
app.brewapp_pid_interval = 5
app.brewapp_p =102
app.brewapp_i =100
app.brewapp_d =5
