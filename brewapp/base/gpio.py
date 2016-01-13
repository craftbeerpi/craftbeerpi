from brewapp import app, socketio, db
from brewapp.base.util import *
from subprocess import call
from step import nextStep, reset

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def initGPIO():
    app.logger.info("## Init GIPO")
    try:
        call(["modprobe", "w1-gpio"])
        call(["modprobe", "w1-therm"])
        for vid in app.brewapp_kettle_state:
            app.logger.info("## Kettle: " + str(vid))
            if(app.brewapp_kettle_state[vid]["heater"]["gpio"] != None):
                app.logger.info("SETUP GPIO HEATER: " + str(app.brewapp_kettle_state[vid]["heater"]["gpio"]))
                GPIO.setup(int(app.brewapp_kettle_state[vid]["heater"]["gpio"]), GPIO.OUT)
                GPIO.output(app.brewapp_kettle_state[vid]["heater"]["gpio"], 1)
            if(app.brewapp_kettle_state[vid]["agitator"]["gpio"] != None):
                app.logger.info("SETUP GPIO AGITATOR" + str(app.brewapp_kettle_state[vid]["agitator"]["gpio"]))
                GPIO.setup(app.brewapp_kettle_state[vid]["agitator"]["gpio"], GPIO.OUT)
                GPIO.output(app.brewapp_kettle_state[vid]["agitator"]["gpio"], 1)
        initHardwareButton()
        app.brewapp_gpio = True
        app.logger.info("ALL GPIO INITIALIZED")
        print "GPIO OK"
    except Exception as e:
        print "GPIO ERROR"
        app.logger.error("SETUP GPIO FAILD " + str(e))
        app.brewapp_gpio = False

## Callback Method for Hardware Button
def nextStepCallback(channel):
    nextStep()

## CallBack Method for Hardware Button
def resetStepCallback(channel):
    reset()

## Setup Hardware Button
def initHardwareButton():
    if(app.brewapp_button != None):
        GPIO.setup(app.brewapp_button["next"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(app.brewapp_button["next"], GPIO.RISING, callback=nextStepCallback, bouncetime=300)
        GPIO.setup(app.brewapp_button["reset"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(app.brewapp_button["reset"], GPIO.RISING, callback=resetStepCallback, bouncetime=300)

def toogle(vid, name, gpio):
    if(app.brewapp_kettle_state[vid][name]["gpio"] == gpio):
        if(app.brewapp_kettle_state[vid][name]["state"] == False):
            switchON(gpio)
            app.brewapp_kettle_state[vid][name]["state"] = True
        else:
            switchOFF(gpio)
            app.brewapp_kettle_state[vid][name]["state"]= False

def switchON(gpio):
    app.logger.info("GPIO ON" + str(gpio))
    if(app.brewapp_gpio == True):
        GPIO.output(gpio, 0)
        pass
    else:
        app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched on" + str(gpio))

def switchOFF(gpio):
    app.logger.info("GPIO OFF" + str(gpio))
    if(app.brewapp_gpio == True):
        GPIO.output(gpio, 1)
        pass
    else:
        app.logger.warning("GPIO TEST MODE ACTIVE. GPIO is not switched off" + str(gpio))
