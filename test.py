from subprocess import call
import RPi.GPIO as GPIO
import time

call(["modprobe", "w1-gpio"])
call(["modprobe", "w1-therm"])

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

time.sleep(5)

GPIO.output(23, 0)

time.sleep(5)

GPIO.output(23, 1)
