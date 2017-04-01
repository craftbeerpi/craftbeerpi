from flask import request
from brewapp.base.devices import *
from brewapp.base.stats import *
from brewapp.base.thermometer import *

from actor import initHardware
from kettle import initKettle
from views import base
from brewapp import app
import json


@base.route('/setup')
def setup():
    return base.send_static_file("setup.html");

@app.route('/api/setup/kettle', methods=['POST'])
def setKettle():
    data =request.get_json()


    Hardware.query.delete()
    Kettle.query.delete()

    for hw in data["hardware"]:
        ks = Hardware(id=hw["id"], name=hw["name"], type=hw["type"], config=json.dumps(hw["config"]))
        db.session.add(ks)

    for k in data["kettle"]:
        ks = Kettle(name=k.get("name", "Non-Name"), target_temp=0, automatic="null", sensorid=k.get("sensorid", None), agitator=k.get("agitator", None), heater=k.get("heater", None), diameter=50, height=50)
        db.session.add(ks)
    db.session.commit()

    setConfigParameter("BREWERY_NAME", data["brewery_name"]);
    setConfigParameter("SETUP", "No");
    initKettle()
    initHardware(True)
    sendStats()
    return ('', 204)

@app.route('/api/setup/thermometer', methods=['POST'])
def setThermometer():
    data =request.get_json()
    thermometer = {
        'DUMMY': dummy_thermometer.DummyThermometer(),
        '1WIRE': w1_thermometer.OneWireThermometer(),
    }
    app.brewapp_thermometer = thermometer.get(data["type"], dummy_thermometer.DummyThermometer())
    setConfigParameter("THERMOMETER_TYPE",data["type"] )
    return json.dumps(app.brewapp_thermometer.getSensors())

@app.route('/api/setup/hardware', methods=['POST'])
def setHardware():
    data =request.get_json()
    hardware= {
        'DUMMY': dummygpio.DummyGPIO(),
        'GPIO': gpio.BrewGPIO(),
        'GEMBIRD': gembird.GembirdUSB(),
        'PIFACE': piface.PiFace(),
        'CHIP-GPIO': chip_gpio.BrewGPIO(),
        'GPIOSYS': gpiosys.GPIOSys()
    }
    app.brewapp_hardware = hardware.get(data["type"], dummygpio.DummyGPIO())
    setConfigParameter("SWITCH_TYPE",data["type"] )
    return json.dumps(app.brewapp_hardware.getDevices())

def setConfigParameter(name, value):
    config = Config.query.get(name);

    if(config == None):
        config = Config()
        config.name = name
        config.value = value
    else:
        config.value = value

    app.brewapp_config[name] = value

    db.session.add(config)
    db.session.commit()
