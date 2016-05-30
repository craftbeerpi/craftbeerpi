from flask import Blueprint, render_template, jsonify, request
from util import *
from model import *
from brewapp import app, socketio
from views import base
from brewapp import manager
from flask.ext.restless.helpers import to_dict

@app.route('/api/hardware/state', methods=['GET'])
def pumpstate():
    return  json.dumps(app.brewapp_pump_state)


def pre_post(data, **kw):
    if(data["config"] != None):
        data["config"] = json.dumps(data["config"])

def post_post(result=None, **kw):
    if(result["config"] != None):
        result["config"] = json.loads(result["config"])
    initHardware()

def post_get_single(result=None, **kw):
    if(result["config"] != None):
        result["config"] = json.loads(result["config"])

def post_get_many(result, **kw):
    for o in result["objects"]:
        if(o["config"] != None):
            o["config"] = json.loads(o["config"])

@brewinit(100)
def init2():
    if(app.createdb == False):
        app.brewapp_hardware.init()
        app.brewapp_thermometer.init()

@brewinit()
def init():

    manager.create_api(Hardware, methods=['GET', 'POST', 'DELETE', 'PUT'],
    preprocessors={
        'POST': [pre_post],
        'PATCH_SINGLE': [pre_post]},
    postprocessors={
        'POST': [post_post],
        'GET_MANY': [post_get_many],
        'GET_SINGLE': [post_get_single],
        'PATCH_SINGLE': [post_post],
    })
    initHardware(False)

def initHardware(cleanup = True):

    app.brewapp_switch_state = {}
    app.brewapp_hardware_config = {}
    hw = Hardware.query.all()

    for h in hw:
        h1 = to_dict(h)
        if(h1['config'] != None):
            h1['config'] = json.loads(h1['config'])
            app.brewapp_hardware_config[h1['switch']] = h1
        if(h.switch != None):
            app.brewapp_switch_state[h.switch] = False


    if(cleanup):
        app.brewapp_hardware.cleanup()
        app.brewapp_hardware.init()


@app.route('/api/switch', methods=['GET'])
def switchstate():
    return  json.dumps(app.brewapp_switch_state)

@socketio.on('switch', namespace='/brew')
def ws_switch(data):
    s = data["switch"]
    if(app.brewapp_switch_state[s] == True):
        app.logger.info("Switch off: " + str(s))
        app.brewapp_hardware.switchOFF(s);
        app.brewapp_switch_state[s] = False
    else:
        app.logger.info("Switch on: " + str(s))
        app.brewapp_hardware.switchON(s);
        app.brewapp_switch_state[s]  = True

    socketio.emit('switch_state_update', app.brewapp_switch_state, namespace ='/brew')


def switchOn(s):
    app.brewapp_hardware.switchON(s);
    app.brewapp_switch_state[s]  = True
    socketio.emit('switch_state_update', app.brewapp_switch_state, namespace ='/brew')

def switchOff(s):
    app.brewapp_hardware.switchOFF(s);
    app.brewapp_switch_state[s]  = False
    socketio.emit('switch_state_update', app.brewapp_switch_state, namespace ='/brew')


class SwitchBase(object):

    state = False

    def init(self):
        pass

    def cleanup(self):
        pass

    def getDevices(self):
        gpio = []
        for i in range(1, 6):
            gpio.append("GPIO"+str(i))
        return gpio

    def getConfig(self, device):
        return app.brewapp_hardware_config[device].get("config", None)

    def getConfigValue(self, device, parameter, default):
        cfg = self.getConfig(device)
        if(cfg != None):
            return cfg.get(parameter, default)
        else:
            return default

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))


    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
