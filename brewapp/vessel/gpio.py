from brewapp import app, socketio, db
from brewapp.base.util import *
from subprocess import call



def initGPIO():
    try:
        call(["modprobe", "w1-gpio"])
        call(["modprobe", "w1-therm"])
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        for vid in app.brewapp_vessel:
            if(app.brewapp_vessel[vid]["heater"]["gpio"] != None):
                print "SETUP GPIO HEATER", app.brewapp_vessel[vid]["heater"]["gpio"]
                GPIO.setup(int(app.brewapp_vessel[vid]["heater"]["gpio"]), GPIO.OUT)
                GPIO.output(app.brewapp_vessel[vid]["heater"]["gpio"], 1)
            if(app.brewapp_vessel[vid]["agitator"]["gpio"] != None):
                print "SETUP GPIO AGITATOR", app.brewapp_vessel[vid]["agitator"]["gpio"]
                GPIO.setup(app.brewapp_vessel[vid]["agitator"]["gpio"], GPIO.OUT)
                GPIO.output(app.brewapp_vessel[vid]["agitator"]["gpio"], 1)
        app.brewapp_gpio = True
    except ImportError:
        print  "     -->GPIO SETUP FAILED"
        app.brewapp_gpio = False

def switchON(gpio):
    print "GPIO ON", gpio
    if(app.brewapp_gpio == True):
        GPIO.output(23, 0)

def switchOFF(gpio):
    print "GPIO OFF", gpio
    if(app.brewapp_gpio == True):
        GPIO.output(23, 1)
