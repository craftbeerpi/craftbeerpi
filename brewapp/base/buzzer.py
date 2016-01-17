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
    start_new_thread(sound3,(,))
    


@start_timer.connect_via(app)
def timer(sender, **extra):
    sound()

@reset_step.connect_via(app)
def reset(sender, **extra):
    sound2()

def sound2():
    try:
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(buzzer_gpio,GPIO.LOW)
    except Exception as e:
        print e

def sound3():
    wait = .2
    try:
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer_gpio,GPIO.LOW)
        time.sleep(wait)
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer_gpio,GPIO.LOW)
        time.sleep(wait)
        GPIO.output(buzzer_gpio,GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(buzzer_gpio,GPIO.LOW)
    except Exception as e:
        print e

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
