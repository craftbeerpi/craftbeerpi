from brewapp import app

app.brewapp_jobs = []
app.brewapp_init = []
app.brewapp_gpio = False
app.testMode = True
app.brewapp_jobstate = {}
app.brewapp_current_step = None
app.brewapp_button = {"next": 23, "reset": 24}
app.brewapp_kettle_state = {}
app.brewapp_kettle_temps_log = {}
app.brewapp_kettle_automatic = {}
app.brewapp_pid_state =  {}
