from brewapp import app

app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_gpio = False
app.brewapp_thermometer = {}
app.brewapp_steps = None
app.brewapp_chartdata = {}
app.brewapp_temperature = {}
app.testMode = False
app.brewapp_jobstate = {}
app.brewapp_current_step = None
app.brewapp_gpio_state = {}
app.brewapp_thermometer_recording = True;
app.brewapp_log = []
#app.brewapp_kettle = []
app.brewapp_log_method = None


### NEW PARAMS
app.brewapp_kettle_state = {}
app.brewapp_kettle_temps_log = {}


## JOBS
app.brewapp_jobs2 = []
app.brewapp_jobstate2 = {}

## Step
app.brewapp_current_step = None
app.brewapp_kettle_automatic = {}

app.brewapp_pid_state =  {}
#app.brewapp_kettle = []
