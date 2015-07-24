from brewapp import app, socketio
from flask import render_template
import json
from brewapp.model import db, Step, Temperatur, Log, Config
import globalprops
from flask.ext.socketio import SocketIO, emit
from datetime import datetime, timedelta


## Cache for states
gpio_state = {}

#Set method for GPIO. Populates the cache
def setupGPIO():
	try:
		import RPi.GPIO as GPIO
		GPIO.setmode(GPIO.BCM)
		gpios = Config.query.filter(Config.name.like("gpio_%")).all()
		for g in gpios:
			d = json.loads(g.value)
			#GPIO.setup(int(g.value), GPIO.OUT)
			gpio_state[g.name] = False
		print "GPIO = TRUE"
		globalprops.gpioMode = True
	except ImportError:
		print "GPIO SETUP ERROR"
    	globalprops.gpioMode = False

## call setup
setupGPIO()

def getAllGPIO():
	gpio_config = []
	gpios = Config.query.filter(Config.name.like("gpio_%")).all()
	for g in gpios:
		d = json.loads(g.value)
		try:
			state = gpio_state[g.name]
		except:
			gpio_state[g.name] = False
			state = False
		gpio_config.append({"label": d["label"], "state": state, "id" : g.name})
	return gpio_config

@app.route("/gpio/<item>/<state>")
def httpGpio(item = None, state = None):
	return setState(item, state)

def addMessage(message):
    l = Log()
    l.text = message
    l.time = datetime.utcnow()

    db.session.add(l)
    db.session.commit()
    # Update all connected clients
    socketio.emit('logupdate', l.to_json(), namespace ='/brew')

def setState(item = None, state = None, logmsg = True):

	global gpio_state

	if(item.startswith("gpio_") == False):
		parameter_name = "gpio_"+item
	else:
		parameter_name = item

	pin = Config.getParameter(parameter_name, "{\"pin\":-1}", True)

	## Check if pin is configured
	if(pin['pin'] == -1):
		return "NO PIN CONFIGURED"
	## Check if command is on, off or toggle
 	if(state != "on" and state != "off" and state != "toggle"):
 		return "Wrong command"

	## try to read the current state
	try:
		old_state = gpio_state[parameter_name]
		if(state == "on"):
			if(gpio_state[parameter_name] == False):
				gpio_state[parameter_name] = True
		elif(state == "off"):
			if(gpio_state[parameter_name] == True):
				gpio_state[parameter_name] = False
		else:
			if(gpio_state[parameter_name] == False):
				gpio_state[parameter_name] = True
			else:
				gpio_state[parameter_name] = False
	except:
		## no state on server side
		gpio_state[parameter_name] = None
		old_state = None
		if(state == "on" or state == "toggle"):
			print "Switch on"
			gpio_state[parameter_name] = True
		elif(state == "off"):
			print "switch off"
			gpio_state[parameter_name] = False

	if(gpio_state[parameter_name] != old_state):
		if(gpio_state[parameter_name] == True):
			suffix = " ein"
		else:
			suffix = " aus"
		#if(logmsg):
		#	addMessage(pin['label'] + suffix)
		if(globalprops.gpioMode):
			GPIO.output(pin['pin'], gpio_state[parameter_name])
		socketio.emit('gpio_update', getAllGPIO(), namespace ='/brew')
		return True
	else:
		return False

@socketio.on('gpio', namespace='/brew')
def ws_gpio(name):
    result = setState(name,"toggle")
