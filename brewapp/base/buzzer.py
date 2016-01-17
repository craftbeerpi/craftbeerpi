from signals import *
from brewapp import app
from views import base
from util import *
import time

buzzer_gpio = 21

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    app.logger.info("SETUP GPIO Module Loaded")
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))
    pass

@brewinit()
def initBuzzer():
    print "INIT"
    try:
        GPIO.setup(buzzer_gpio, GPIO.OUT)
        GPIO.output(buzzer_gpio, 0)
    except Exception as e:
        print e

@next_step.connect_via(app)
def nextStepBeep(sender, **extra):
    print "NEXT"
    #Dot Dot Dot
    sound()


@start_timer.connect_via(app)
def timer(sender, **extra):
    print "TIMER"
    sound()

@reset_step.connect_via(app)
def reset(sender, **extra):
    print "REST"
    sound()

def sound():
    try:
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(buzzer_gpio,GPIO.LOW)
        time.sleep(.1)
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(buzzer_gpio,GPIO.LOW)
        time.sleep(.1)
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(.1)

        GPIO.output(buzzer_gpio,GPIO.LOW)
    except Exception as e:
        print e
