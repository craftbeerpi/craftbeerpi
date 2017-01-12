import time
import lcddriver
from brewapp import app
from brewapp.base import Config
from brewapp.base.util import brewinit, brewjob

try:
    import RPi.GPIO as GPIO
    app.logger.info("SETUP GPIO Module Loaded")
    from time import time
    from time import sleep
    from datetime import datetime
    lcd = lcddriver.lcd()
    # GPIO PINS
    LCD_SCA = 8
    LCD_SCL = 9
except Exception as e:
    app.logger.error("SETUP GPIO Module " + str(e))


@brewinit()
def init_lcd():
    app.logger.info("--> I2C --> INIT")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_SCA, GPIO.OUT)
    GPIO.setup(LCD_SCL, GPIO.OUT)
    
    lcd.clear();

    pass

@brewjob(key="lcdjob", interval=1)
def lcdjob():


    if (app.brewapp_current_step == None):
        lcd.display_string("CraftBeerPi 2.2", 1)
        lcd.display_string(app.brewapp_config.get("BREWERY_NAME"), 2)
        return

    ## get current step
    cs = app.brewapp_current_step
    ## get thermometerid
    id = int(app.brewapp_kettle_state[cs.get("kettleid")]["sensorid"])
    ## get current temp
    current_temp = app.brewapp_thermometer_last[id]

    #update display
    lcd.display_string(cs.get("name"), 1)
    lcd.display_string("Current Temp: %s" % (current_temp), 2)
    lcd.display_string("Target Temp: %s" % (cs.get("temp")), 3)
