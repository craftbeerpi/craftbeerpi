from brewapp import app, socketio, db
from brewapp.base.util import *

def initGPIO():
    try:
        import RPi.GPIO as GPIO # Import GPIO
        GPIO.setmode(GPIO.BCM)
        for vid in app.brewapp_vessel:
            if(app.brewapp_vessel[vid]["heater"]["gpio"] != None):
                print "SETUP GPIO HEATER", app.brewapp_vessel[vid]["heater"]["gpio"]
                #GPIO.setup(app.brewapp_vessel[vid]["agitator"]["gpio"], GPIO.OUT)
            if(app.brewapp_vessel[vid]["agitator"]["gpio"] != None):
                print "SETUP GPIO AGITATOR", app.brewapp_vessel[vid]["agitator"]["gpio"]
                #GPIO.setup(app.brewapp_vessel[vid]["agitator"]["gpio"], GPIO.OUT)
        app.brewapp_gpio = True
    except ImportError:
        print  "     -->GPIO SETUP FAILED"
        app.brewapp_gpio = False

def switchON(gpio):
    print "GPIO ON", gpio
    if(app.brewapp_gpio == True):
        GPIO.output(gpio, True)

def switchOFF(gpio):
    print "GPIO OFF", gpio
    if(app.brewapp_gpio == True):
        GPIO.output(gpio, False)
