from flask import Blueprint, render_template, jsonify, request
from util import *
from model import *
from brewapp import app, socketio
from views import base
from brewapp import manager

@app.route('/api/hardware/state', methods=['GET'])
def pumpstate():
    return  json.dumps(app.brewapp_pump_state)

def post_post(result=None, **kw):
    initHardware()

@brewinit(100)
def init2():
    if(app.createdb == False):
        app.brewapp_hardware.init()
        app.brewapp_thermometer.init()

@brewinit()
def init():

    manager.create_api(Hardware, methods=['GET', 'POST', 'DELETE', 'PUT'],
    postprocessors={
        'POST': [post_post],
        'PATCH_SINGLE': [post_post],
    })
    initHardware(False)

def initHardware(cleanup = True):
    if(cleanup):
        app.brewapp_hardware.cleanup()
        app.brewapp_hardware.init()

    app.brewapp_switch_state = {}
    hw = Hardware.query.all()
    for h in hw:
        if(h.switch != None):
            app.brewapp_switch_state[h.switch] = False

    kettles = Kettle.query.all()
    for v in kettles:
        if(v.agitator != None):
            app.brewapp_switch_state[v.agitator] = False
        if(v.heater != None):
            app.brewapp_switch_state[v.heater] = False

    print app.brewapp_switch_state

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

    def switchON(self, device):
        app.logger.info("GPIO ON" + str(device))


    def switchOFF(self, device):
        app.logger.info("GPIO OFF" + str(device))
