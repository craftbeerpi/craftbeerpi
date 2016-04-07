from brewapp import app
from brewapp.base.devices import *
from brewapp.base.thermometer import *
from brewapp.base.automatic import *

from model import *

def initDriver():
    print "INIT DRIVER"
    hardware= {
        'DUMMY': dummygpio.DummyGPIO(),
        'GPIO': gpio.BrewGPIO(),
        'GEMBIRD': gembird.GembirdUSB(),
        'PIFACE': piface.PiFace(),
    }

    thermometer = {
        'DUMMY': dummy_thermometer.DummyThermometer(),
        '1WIRE': w1_thermometer.OneWireThermometer(),
    }
    
    app.brewapp_hardware = hardware.get(app.brewapp_config.get("SWITCH_TYPE", "DUMMY"), dummygpio.DummyGPIO())
    app.brewapp_thermometer = thermometer.get(app.brewapp_config.get("THERMOMETER_TYPE", "DUMMY"), dummy_thermometer.DummyThermometer())

    print app.brewapp_hardware
    print app.brewapp_thermometer
