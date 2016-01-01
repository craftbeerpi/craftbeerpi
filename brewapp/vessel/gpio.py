from brewapp import app, socketio, db
from brewapp.base.util import *

@brewinit()
def initGPIO():
    try:
        import RPi.GPIO as GPIO # Import GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        app.brewapp_gpio = True

    except ImportError:
        print  "GPIO ERROR"
        app.brewapp_gpio = False

def switchON(gpio):
    print "GPIO ON", gpio

def switchOFF(gpio):
    print "GPIO OFF", gpio
