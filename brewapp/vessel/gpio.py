from brewapp import app, socketio, db
from brewapp.base.util import *
from subprocess import call

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(23, GPIO.OUT)
    #GPIO.output(23, 0)
except:
    pass

def initGPIO():
    try:
        call(["modprobe", "w1-gpio"])
        call(["modprobe", "w1-therm"])
        print "###### SETUP GPIO 2 #######"
        #GPIO.setup(23, GPIO.OUT)
        for vid in app.brewapp_vessel:
            if(app.brewapp_vessel[vid]["heater"]["gpio"] != None):
                print "SETUP GPIO HEATER", app.brewapp_vessel[vid]["heater"]["gpio"]
                GPIO.setup(int(app.brewapp_vessel[vid]["agitator"]["gpio"]), GPIO.OUT)
                GPIO.output(app.brewapp_vessel[vid]["agitator"]["gpio"], 1)
            if(app.brewapp_vessel[vid]["agitator"]["gpio"] != None):
                print "SETUP GPIO AGITATOR", app.brewapp_vessel[vid]["agitator"]["gpio"]
                GPIO.setup(app.brewapp_vessel[vid]["agitator"]["gpio"], GPIO.OUT)
        app.brewapp_gpio = True
    except ImportError:
        print  "     -->GPIO SETUP FAILED"
        app.brewapp_gpio = False

def switchON(gpio):
    print app.brewapp_gpio
    print "GPIO ON", gpio
    if(app.brewapp_gpio == True):
        print "TRUE"
        GPIO.output(23, 1)

def switchOFF(gpio):
    print "GPIO OFF", gpio
    if(app.brewapp_gpio == True):
        print "FALSE"
        GPIO.output(23, 0)
