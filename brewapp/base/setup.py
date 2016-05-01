from flask import Blueprint, render_template, jsonify,redirect, url_for, request
import json
from brewapp import app, socketio
from util import *
from model import *
from views import base
from brewapp.base.devices import *
from kettle import initKettle
from hardwareswitch import initHardware
from brewapp.base.devices import *
from brewapp.base.thermometer import *

@base.route('/setup')
def setup():
    return base.send_static_file("setup.html");

@app.route('/api/setup/kettle', methods=['POST'])
def setKettle():
    data =request.get_json()

    for k in data["kettles"]:
        print k
        ks = Kettle(name=k["name"], automatic="null", sensorid=k.get("sensorid",""), target_temp=0, agitator=k.get("agitator",""), heater=k.get("heater",""), height=k.get("height",""), diameter=k.get("diameter",""))
        db.session.add(ks)

    db.session.commit()
    initKettle()
    initHardware(True)
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

    db.session.add(config)
    db.session.commit()
