from util import *
from model import *
from brewapp import app, socketio, manager

import json

def pre_post(data, **kw):

    if data["type"] is "json":
        data["value"] = json.dumps(data["value"])


def post_post(result, **kw):
    if result["type"] is "json":
        result["value"] = json.loads(result["value"])
    readConfig()
    socketio.emit('config', app.brewapp_config, namespace='/brew')


def post_get_many(result, **kw):
    for o in result["objects"]:
        if o["type"] is "json":
            o["value"] = json.loads(o["value"])

    result["objects"] = sorted(result["objects"], key=lambda k: k['name'])


def readConfig():
    app.brewapp_config = {}
    config = Config.query.all()
    for c in config:
        app.brewapp_config[c.name] = c.value


@brewinit(order=-1000)
def init():
    manager.create_api(Config, methods=['GET', 'POST', 'DELETE', 'PUT'],
    preprocessors={
    'POST':[pre_post],
    'PATCH_SINGLE': [pre_post]},
    postprocessors={
    'POST':[post_post],
    'GET_MANY': [post_get_many],
    'GET_SINGLE':[post_post],
    'PATCH_SINGLE': [post_post]})
    readConfig()

from brewapp.base.devices import *
from brewapp.base.thermometer import *

@brewinit(order=-1001)
def initDriver():
    if(app.createdb is False):
       return



    db.session.add(Config(name="BUZZER_GPIO", value="23", type="", default="23", description="Buzzer GPIO"))
    db.session.add(Config(name="BREWNAME", value="", type="", default="", description="Brew Name"))
    db.session.add(Config(name="UNIT", value="C", type="", default="C", description="Thermometer unit", options="C,F"))
    db.session.add(Config(name="THERMOMETER_TYPE", value="1WIRE", type="", default="1WIRE", description="Thermometer Type !!RESTART AFTER CHANGE OF THIS PARAMETER!!!", options="1WIRE,USB,DUMMY"))
    db.session.add(Config(name="SWITCH_TYPE", value="GPIO", type="", default="GPIO", description="Hardware Control type. !!!RESTART AFTER CHANGE OF THIS PARAMETER!!!", options="GPIO,PIFACE,GEMBIRD,DUMMY"))
    db.session.add(Config(name="SEND_STATS", value="True", type="", default="True", description="Sending statistic informaiton to CraftBeerPI. This helps to improve CraftBeerPI in the future", options="True,False"))
    db.session.add(Config(name="USE_LCD", value="False", type="", default="False", description="Activate LCD display control", options="True,False"))
    db.session.add(Config(name="BREWERY_NAME", value="", type="", default="", description="Name of your Berwery"))
    db.session.add(Config(name="USERNAME", value="admin", type="", default="admin", description="Login User"))
    db.session.add(Config(name="PASSWORD", value="123", type="", default="123", description="Login Password"))
    db.session.add(Config(name="THEME", value="static/themes/dark-theme.css", type="", default="static/themes/dark-theme.css", description="UI Theme", options="static/themes/dark-theme.css,static/themes/blue-theme.css,"))
    db.session.commit()


@brewinit()
def initDriver():
    app.logger.info("INIT Driver")

    hardware= {
        'DUMMY': dummygpio.DummyGPIO(),
        'GPIO': gpio.BrewGPIO(),
        'GEMBIRD': gembird.GembirdUSB(),
        'PIFACE': piface.PiFace(),
    }

    thermometer = {
        'DUMMY': dummy_thermometer.DummyThermometer(),
        '1WIRE': w1_thermometer.OneWireThermometer(),
        'USB': usb_thermometer.USBThermometer()
    }

    app.brewapp_hardware = hardware.get(app.brewapp_config.get("SWITCH_TYPE", "DUMMY"), dummygpio.DummyGPIO())
    app.brewapp_thermometer = thermometer.get(app.brewapp_config.get("THERMOMETER_TYPE", "DUMMY"), dummy_thermometer.DummyThermometer())
    app.logger.info(app.brewapp_hardware )
    app.logger.info(app.brewapp_thermometer )
